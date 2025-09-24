from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services.sueldo_liquido_service import calculo_sueldo_liquido, calculo_sueldo_bruto_desde_liquido


class CalculoSueldoLiquidoView(APIView):
    """
    Endpoint para calcular el sueldo líquido de un colaborador.
    
    Este endpoint recibe los parámetros necesarios para calcular el sueldo líquido
    incluyendo descuentos de AFP, salud, cesantía e impuestos, además de las asignaciones
    correspondientes.
    """
    
    @swagger_auto_schema(
        operation_description="Calcula el sueldo líquido basado en los parámetros proporcionados",
        operation_summary="Cálculo de Sueldo Líquido",
        tags=['Salary'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sueldo_base', 'tipo_contrato', 'afp'],
            properties={
                'sueldo_base': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Sueldo base del colaborador',
                    example=800000
                ),
                'tipo_contrato': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Tipo de contrato (1: Indefinido, 2: Plazo fijo, etc.)',
                    example=1
                ),
                'afp': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='AFP del colaborador (Capital, Cuprum, Habitat, Modelo, Planvital, Provida, Uno)',
                    example='Capital'
                ),
                'salud': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Sistema de salud (Fonasa o nombre de Isapre)',
                    default='Fonasa',
                    example='Fonasa'
                ),
                'gratificacion': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de gratificación',
                    default=0,
                    example=50000
                ),
                'asignacion_familiar': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de asignación familiar',
                    default=0,
                    example=12364
                ),
                'asignacion_colacion': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de asignación de colación',
                    default=0,
                    example=30000
                ),
                'asignacion_transporte': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de asignación de transporte',
                    default=0,
                    example=25000
                ),
                'asignacion_otros': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Otros montos de asignaciones',
                    default=0,
                    example=10000
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Cálculo exitoso del sueldo líquido",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'haberes': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'sueldo_base': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'gratificacion': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_familiar': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_colacion': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_transporte': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_otros': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'Total haberes': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'deberes': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'descuento_afp': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'descuento_salud': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'descuento_cesantia': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'impuesto': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'Total descuentos': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'sueldo_liquido': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'indicadores': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'utm': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'uf': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Error en los parámetros de entrada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            500: openapi.Response(
                description="Error interno del servidor",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Calcula el sueldo líquido basado en los parámetros proporcionados.
        
        Realiza todos los cálculos necesarios incluyendo:
        - Descuentos previsionales (AFP, Salud, Cesantía)
        - Cálculo de impuesto único
        - Asignaciones familiares y otras
        - Sueldo líquido final
        """
        try:
            # Validar parámetros requeridos
            required_fields = ['sueldo_base', 'tipo_contrato', 'afp']
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {'detail': f'El campo "{field}" es requerido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Extraer parámetros del request
            sueldo_base = request.data.get('sueldo_base')
            tipo_contrato = request.data.get('tipo_contrato')
            afp = request.data.get('afp')
            salud = request.data.get('salud', 'Fonasa')
            gratificacion = request.data.get('gratificacion', 0)
            asignacion_familiar = request.data.get('asignacion_familiar', 0)
            asignacion_colacion = request.data.get('asignacion_colacion', 0)
            asignacion_transporte = request.data.get('asignacion_transporte', 0)
            asignacion_otros = request.data.get('asignacion_otros', 0)
            
            # Validar tipos de datos
            try:
                sueldo_base = float(sueldo_base)
                tipo_contrato = int(tipo_contrato)
                gratificacion = float(gratificacion) if gratificacion else 0
                asignacion_familiar = float(asignacion_familiar) if asignacion_familiar else 0
                asignacion_colacion = float(asignacion_colacion) if asignacion_colacion else 0
                asignacion_transporte = float(asignacion_transporte) if asignacion_transporte else 0
                asignacion_otros = float(asignacion_otros) if asignacion_otros else 0
            except (ValueError, TypeError):
                return Response(
                    {'detail': 'Los valores numéricos deben ser válidos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar valores mínimos
            if sueldo_base <= 0:
                return Response(
                    {'detail': 'El sueldo base debe ser mayor a 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar AFP válida
            afps_validas = ['Capital', 'Cuprum', 'Habitat', 'Modelo', 'Planvital', 'Provida', 'Uno']
            if afp not in afps_validas:
                return Response(
                    {'detail': f'AFP debe ser una de: {", ".join(afps_validas)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Realizar el cálculo
            resultado = calculo_sueldo_liquido(
                sueldo_base=sueldo_base,
                tipo_contrato=tipo_contrato,
                afp=afp,
                salud=salud,
                gratificacion=gratificacion,
                asignacion_familiar=asignacion_familiar,
                asignacion_colacion=asignacion_colacion,
                asignacion_transporte=asignacion_transporte,
                asignacion_otros=asignacion_otros
            )
            
            return Response(resultado, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en cálculo de sueldo líquido: {str(e)}")
            
            return Response(
                {'detail': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CalculoSueldoBrutoDesdeNeto(APIView):
    """
    Endpoint para calcular el sueldo bruto (sueldo base) necesario para obtener un sueldo líquido específico.
    
    Este endpoint utiliza un algoritmo iterativo que estima el sueldo base requerido para alcanzar
    el sueldo líquido deseado, considerando todos los descuentos e impuestos aplicables.
    """
    
    @swagger_auto_schema(
        operation_description="Calcula el sueldo bruto necesario para obtener un sueldo líquido específico mediante iteración",
        operation_summary="Cálculo Inverso: Sueldo Bruto desde Sueldo Líquido",
        tags=['Salary'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sueldo_liquido_deseado', 'tipo_contrato', 'afp'],
            properties={
                'sueldo_liquido_deseado': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Sueldo líquido objetivo que se desea obtener',
                    example=600000
                ),
                'tipo_contrato': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Tipo de contrato (1: Indefinido, 2: Plazo fijo, etc.)',
                    example=1
                ),
                'afp': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='AFP del colaborador (Capital, Cuprum, Habitat, Modelo, Planvital, Provida, Uno)',
                    example='Capital'
                ),
                'salud': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Sistema de salud (Fonasa o nombre de Isapre)',
                    default='Fonasa',
                    example='Fonasa'
                ),
                'gratificacion': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description='Indica si se aplica gratificación',
                    default=False,
                    example=False
                ),
                'asignacion_familiar': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de asignación familiar',
                    default=0,
                    example=12364
                ),
                'asignacion_colacion': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de asignación de colación',
                    default=0,
                    example=30000
                ),
                'asignacion_transporte': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Monto de asignación de transporte',
                    default=0,
                    example=25000
                ),
                'asignacion_otros': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Otros montos de asignaciones',
                    default=0,
                    example=10000
                ),
                'tolerancia': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Diferencia máxima aceptable entre sueldo líquido calculado y deseado',
                    default=100.0,
                    example=100.0
                ),
                'max_iteraciones': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Número máximo de iteraciones del algoritmo',
                    default=100,
                    example=100
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Cálculo exitoso del sueldo bruto",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'haberes': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'sueldo_base': openapi.Schema(type=openapi.TYPE_NUMBER, description='Sueldo base calculado'),
                                'gratificacion': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_familiar': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_colacion': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_transporte': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'asignacion_otros': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'Total haberes': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'deberes': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'descuento_afp': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'descuento_salud': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'descuento_cesantia': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'impuesto': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'Total descuentos': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'sueldo_liquido': openapi.Schema(type=openapi.TYPE_NUMBER, description='Sueldo líquido obtenido'),
                        'indicadores': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'utm': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'uf': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'calculo_inverso': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'sueldo_liquido_deseado': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'sueldo_liquido_obtenido': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'diferencia_final': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'iteraciones_realizadas': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'convergencia_exitosa': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'tolerancia_utilizada': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'sueldo_base_calculado': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Error en los parámetros de entrada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            500: openapi.Response(
                description="Error interno del servidor",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Calcula el sueldo bruto necesario para obtener un sueldo líquido específico.
        
        Utiliza un algoritmo iterativo que:
        1. Estima un sueldo base inicial (sueldo líquido * 1.25)
        2. Calcula el sueldo líquido resultante
        3. Ajusta el sueldo base según la diferencia
        4. Repite hasta convergencia o máximo de iteraciones
        """
        try:
            # Validar parámetros requeridos
            required_fields = ['sueldo_liquido_deseado', 'tipo_contrato', 'afp']
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {'detail': f'El campo "{field}" es requerido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Extraer parámetros del request
            sueldo_liquido_deseado = request.data.get('sueldo_liquido_deseado')
            tipo_contrato = request.data.get('tipo_contrato')
            afp = request.data.get('afp')
            salud = request.data.get('salud', 'Fonasa')
            gratificacion = request.data.get('gratificacion', False)
            asignacion_familiar = request.data.get('asignacion_familiar', 0)
            asignacion_colacion = request.data.get('asignacion_colacion', 0)
            asignacion_transporte = request.data.get('asignacion_transporte', 0)
            asignacion_otros = request.data.get('asignacion_otros', 0)
            tolerancia = request.data.get('tolerancia', 100.0)
            max_iteraciones = request.data.get('max_iteraciones', 100)
            
            # Validar tipos de datos
            try:
                sueldo_liquido_deseado = float(sueldo_liquido_deseado)
                tipo_contrato = int(tipo_contrato)
                gratificacion = bool(gratificacion)
                asignacion_familiar = float(asignacion_familiar) if asignacion_familiar else 0
                asignacion_colacion = float(asignacion_colacion) if asignacion_colacion else 0
                asignacion_transporte = float(asignacion_transporte) if asignacion_transporte else 0
                asignacion_otros = float(asignacion_otros) if asignacion_otros else 0
                tolerancia = float(tolerancia)
                max_iteraciones = int(max_iteraciones)
            except (ValueError, TypeError):
                return Response(
                    {'detail': 'Los valores numéricos deben ser válidos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar valores mínimos
            if sueldo_liquido_deseado <= 0:
                return Response(
                    {'detail': 'El sueldo líquido deseado debe ser mayor a 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if tolerancia <= 0:
                return Response(
                    {'detail': 'La tolerancia debe ser mayor a 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if max_iteraciones <= 0 or max_iteraciones > 1000:
                return Response(
                    {'detail': 'El número máximo de iteraciones debe estar entre 1 y 1000'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar AFP válida
            afps_validas = ['Capital', 'Cuprum', 'Habitat', 'Modelo', 'Planvital', 'Provida', 'Uno']
            if afp not in afps_validas:
                return Response(
                    {'detail': f'AFP debe ser una de: {", ".join(afps_validas)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Realizar el cálculo inverso
            resultado = calculo_sueldo_bruto_desde_liquido(
                sueldo_liquido_deseado=sueldo_liquido_deseado,
                tipo_contrato=tipo_contrato,
                afp=afp,
                salud=salud,
                gratificacion=gratificacion,
                asignacion_familiar=asignacion_familiar,
                asignacion_colacion=asignacion_colacion,
                asignacion_transporte=asignacion_transporte,
                asignacion_otros=asignacion_otros,
                tolerancia=tolerancia,
                max_iteraciones=max_iteraciones
            )
            
            return Response(resultado, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en cálculo inverso de sueldo: {str(e)}")
            
            return Response(
                {'detail': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )