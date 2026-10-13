from rest_framework import viewsets, status
from gestion_usuarios.models import Usuario
#from gestion_usuarios.serializers import UsuarioSerializer SE CORRIGIÓ ESTA IMPORTACION PORQUE UsuarioSerializer no esta hecho como tal
from gestion_usuarios.serializers import UsuarioCompletoSerializer as UsuarioSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from gestion_usuarios.DAO.usuarioDAO import UsuarioDAO
from gestion_usuarios.serializers import (
    UsuarioCompletoSerializer,
    UsuarioParcialSerializer,
    UsuarioContrasenaSerializer,
    PasswordResetRequestSerializer,
)
from gestion_usuarios.exceptions.usuarioExeptions import (
    UsuarioNoAutorizado_401,
    UsuarioProhibido_403,
    ErrorInternoServidor_500,
    UsuarioNoEncontrado_404,
    DatosInvalidos_400,
    ConflictoUsuario_409,
)

#codigo 9 de P6 que se configura de forma global
#permission_classes = [IsAuthenticated] se agrega en back_end_django/settings.py
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API para la gestión de Usuarios.
    (La seguridad se aplica de forma global mediante JWT y IsAuthenticated en settings.py).
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioViewSet(viewsets.ViewSet):
    """
    API para la gestión de Usuarios.
    """

    @swagger_auto_schema(
        operation_summary="Obtener todos los usuarios",
        responses={
            200: "Éxito",
            401: "No autorizado",
            403: "Prohibido",
            500: "Error interno del servidor",
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Devuelve una lista de todos los usuarios con soporte para
        paginación, ordenamiento y filtrado de acuerdo a los campos
        de la tabla.
        """
        try:
            usuarios = UsuarioDAO.obtener_todos()
            serializer = UsuarioCompletoSerializer(
                usuarios,
                many=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except UsuarioNoAutorizado_401 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except UsuarioProhibido_403 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #activa un usuario especifico mediante una peticion HTTP de tipo PATCH
    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Activar un usuario",
        responses={
            200: "Usuario activado correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Usuario no encontrado",
        },
    )
    def activate(self, request, pk=None):
        """Activa un usuario estableciendo el campo is_active en true."""
        try:
            usuario = UsuarioDAO.activar_usuario(pk)
            return Response(
                {
                    "mensaje": "Usuario activado correctamente",
                    "usuario": UsuarioParcialSerializer(usuario).data,
                },
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    #Permite obtener los detalles completos de un usuario especifico con una solicitud HTTP GET
    @swagger_auto_schema(
        operation_summary="Obtener un usuario por ID",
        responses={
            200: "Exito",
            401: "No Autorizado",
            403: "Prohibido",
            404: "Usuario no encontrado",
            500: "Error interno del servidor",
        },
    )
    def retrieve(self, request, pk=None):
        """Devuelve un usuario específico si existe."""
        try:
            usuario = UsuarioDAO.obtener_usuario_por_id(pk)
            serializer = UsuarioCompletoSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UsuarioNoAutorizado_401 as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        except UsuarioProhibido_403 as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Activar un usuario",
        responses={
            200: "Usuario activado correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Usuario no encontrado",
        },
    )
    def activate(self, request, pk=None):
        """Activa un usuario estableciendo el campo is_active en true."""
        try:
            usuario = UsuarioDAO.activar_usuario(pk)
            return Response(
            {
                "mensaje": "Usuario activado correctamente",
                "usuario": UsuarioParcialSerializer(usuario).data,
            },
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 

    #Codigo 21: implementa el servicio de recuperación de un usuario a partir de su identificador único:
    #describe claramente las posibles respuestas del servicio, tanto en casos exitosos como en escenarios de error.
    @swagger_auto_schema(
        operation_summary="Obtener un usuario por ID",
        responses={
            200: "Exito",
            401: "No Autorizado",
            403: "Prohibido",
            404: "Usuario no encontrado",
            500: "Error interno del servidor",
        },
    )
    #permite obtener lo detalles completos de un usuario especifico mediante una solicitud HTTP GET
    def retrieve(self, request, pk=None):
        """Devuelve un usuario específico si existe."""
        try:
            usuario = UsuarioDAO.obtener_usuario_por_id(pk)
            serializer = UsuarioCompletoSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UsuarioNoAutorizado_401 as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        except UsuarioProhibido_403 as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Codigo 23: implementa el servicio que permite la creación de un nuevo 
    # usuario en el sistema mediante una solicitud HTTP POST.
    @swagger_auto_schema(
        operation_summary="Crear un nuevo usuario",
        request_body=UsuarioParcialSerializer,
        responses={
            201: "Usuario creado exitosamente",
            400: "Error en la validación",
            409: "Conflicto (nombre de usuario o email ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def create(self, request):
        """Crea un nuevo usuario con la información proporcionada en el cuerpo de la petición."""
        try:
            usuario_dto = UsuarioDAO.crear_usuario(**request.data)
            return Response(
                UsuarioCompletoSerializer(usuario_dto).data,
                status=status.HTTP_201_CREATED,
            )

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except ConflictoUsuario_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #COdigo 25: El código anterior implementa el servicio que permite actualizar completamente los datos de un usuario específico, identificado mediante su id.
    @swagger_auto_schema(
        operation_summary="Actualizar un usuario completamente",
        request_body=UsuarioCompletoSerializer,
        responses={
            200: "Usuario actualizado exitosamente",
            400: "Datos inválidos",
            404: "Usuario no encontrado",
            409: "Conflicto (nombre de usuario o email ya registrado)",
            500: "Error interno del servidor",
        },
    )
    #Este metodo utiliza la anotación @swagger_auto_schema para documentar de manera automática los detalles del servicio en Swagger.
    def update(self, request, pk=None):
        """Actualiza completamente un usuario especificado por su id"""
        try:
            usuarioDTO = UsuarioDAO.actualizar_usuario(pk, **request.data)
            return Response(
                UsuarioCompletoSerializer(usuarioDTO).data,
                status=status.HTTP_200_OK,
            )

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ConflictoUsuario_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Codigo 27:anterior implementa el servicio encargado de eliminar un usuario de forma lógica, es decir, sin borrar físicamente el registro de la base de datos.
    @swagger_auto_schema(
        operation_summary="Elimina un usuario (borrado lógico).",
        responses={
            200: "Usuario eliminado Correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Usuario no encontrado",
        },
    )
    def destroy(self, request, pk=None):
        """Marca el usuario como eliminado sin borrarlo físicamente de la base de datos. Esto se realiza actualizando los campos is_deleted y deleted_at."""
        try:
            UsuarioDAO.eliminar_usuario(pk)
            return Response(
                {"mensaje": "Usuario eliminado correctamente"},
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_summary="Actualizar un usuario (parcial)",
            request_body=UsuarioParcialSerializer,
            responses={
                200: "Usuario actualizado parcialmente",
                400: "Datos inválidos",
                404: "Usuario no encontrado",
                409: "Conflicto (nombre de usuario o email ya registrado)",
                500: "Error interno del servidor",
            },
        )
    def partial_update(self, request, pk=None):
            """Actualiza parcialmente un usuario especificado por su id. Solo se actualizan los campos proporcionados en el cuerpo de la petición."""
            try:
                usuarioDTO = UsuarioDAO.actualizar_usuario_parcial(pk, **request.data)
                return Response(
                    UsuarioParcialSerializer(usuarioDTO).data,
                    status=status.HTTP_200_OK,
                )

            except DatosInvalidos_400 as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            except UsuarioNoEncontrado_404 as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

            except ConflictoUsuario_409 as e:
                return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

            except ErrorInternoServidor_500 as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Codigo 31: implementa el servicio encargado de restaurar un usuario que previamente fue eliminado de forma logica.
    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
    operation_summary="Restaurar un usuario eliminado",
    responses={
        200: "Usuario restaurado correctamente",
        401: "No autorizado",
        400: "Error en la validación",
        404: "Usuario no encontrado",
    },
    )
    def restore(self, request, pk=None):
        """Restaura un usuario que había sido marcado como eliminado lógicamente. Esto se realiza actualizando los campos is_deleted y deleted_at."""
        try:
            usuario = UsuarioDAO.restaurar_usuario(pk)
            return Response(
                {"mensaje": "Usuario restaurado correctamente"},
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #COdigo 33: EL siguiente codigo es encargado de verificar el correo electronico de un usuario especifico:
    @action(detail=True, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Verificar email del usuario",
        responses={
            200: "Email verificado exitosamente",
            401: "No autorizado",
            403: "Prohibido",
            400: "El email ya estaba verificado",
            404: "Usuario no encontrado",
            500: "Error interno del servidor",
        },
    )
    def verify_email(self, request, pk=None):
        """Marca el email de un usuario como verificado y actualiza la fecha de verificación en el campo email_verified_at."""
        try:
            UsuarioDAO.verificar_email(pk)
            return Response(
                {"mensaje": "Email verificado exitosamente"},
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 

    #Codigo 35. Servicio: desactivar usuario especifico en el sistema
    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Desactivar un usuario",
        responses={
            200: "Usuario eliminado Correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Usuario no encontrado",
        },
    )
    def deactivate(self, request, pk=None):
        """Desactiva un usuario estableciendo el campo is_active en false."""
        try:
            UsuarioDAO.desactivar_usuario(pk)
            return Response(
                {"mensaje": "Usuario eliminado correctamente"},
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #Codigo 37. Servicio: cambiar la contraseña del usuario de forma segura-
    @action(detail=True, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Cambiar contraseña del usuario",
        request_body=UsuarioContrasenaSerializer,
        responses={
            200: "Contraseña actualizada correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Usuario no encontrado",
        },
    )
    def change_password(self, request, pk=None):
        """
        Permite a un usuario autenticado cambiar su contraseña proporcionando
        la contraseña actual y una nueva contraseña.
        """
        from django.core.exceptions import ValidationError
        serializer = UsuarioContrasenaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Llama al método para actualizar la contraseña
                UsuarioDAO.actualizar_contrasena(
                    pk,
                    serializer.validated_data["current_password"],
                    serializer.validated_data["new_password"],
                    serializer.validated_data["confirm_password"],
                )
                return Response(
                    {"mensaje": "Contraseña actualizada correctamente"},
                    status=status.HTTP_200_OK,
                )

            except UsuarioNoEncontrado_404 as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

            except ValidationError as e:
                return Response(
                    {"error": e.messages},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Codigo 40: IMplementa el servicio encargado de iniciar el proceso de restablecimiento de contaseñas de un usuario
    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Solicitar restablecimiento de contraseña",
        request_body=PasswordResetRequestSerializer,
        responses={
            200: "Se ha enviado un enlace de restablecimiento a tu correo",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Usuario no encontrado",
        },
    )
    def request_password_reset(self, request):
        """Permite solicitar un restablecimiento de contraseña enviando un enlace o token al correo."""
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]

        try:
            UsuarioDAO.reset_password_request(email)
            return Response(
                {"mensaje": "Se ha enviado un enlace de restablecimiento a tu correo"},
                status=status.HTTP_200_OK,
            )

        except UsuarioNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 