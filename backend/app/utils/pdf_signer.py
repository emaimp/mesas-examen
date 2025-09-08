import os
from pathlib import Path
from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.keys import load_certs_from_pemder, load_private_key_from_pemder

# Directorio donde se guardarán los certificados de prueba
CERTS_DIRECTORY = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / "certs"

# Usaremos un único certificado de prueba global para todos los profesores
GLOBAL_TEST_CERT_KEY_PATH = CERTS_DIRECTORY / "test_professor_firma.key"
GLOBAL_TEST_CERT_CRT_PATH = CERTS_DIRECTORY / "test_professor_firma.crt"
GLOBAL_TEST_CERT_PASSWORD = "test" # La contraseña que usamos al generar el .pfx

async def sign_pdf_with_test_cert(
    pdf_data: bytes,
    output_filepath: Path,
    reason: str = "Firma de Acta Digital",
    location: str = "Universidad"
) -> Path:
    output_filepath_str = str(output_filepath)
    """
    Firma un PDF con el certificado autofirmado de prueba global.

    Args:
        pdf_data: Contenido del PDF a firmar en bytes.
        output_filepath: Ruta donde se guardará el PDF firmado.
        reason: Razón de la firma.
        location: Ubicación de la firma.

    Returns:
        La ruta al PDF firmado.
    """
    if not GLOBAL_TEST_CERT_KEY_PATH.exists() or not GLOBAL_TEST_CERT_CRT_PATH.exists():
        raise FileNotFoundError(
            f"Archivos de clave/certificado de prueba global no encontrados en {CERTS_DIRECTORY}. "
            "Asegúrate de haber ejecutado el comando OpenSSL para generarlos."
        )

    # Cargar la clave privada y el certificado global
    private_key = load_private_key_from_pemder(GLOBAL_TEST_CERT_KEY_PATH, passphrase=GLOBAL_TEST_CERT_PASSWORD.encode('utf-8'))
    certs = list(load_certs_from_pemder(GLOBAL_TEST_CERT_CRT_PATH))
    signer = signers.SimpleSigner(
        signing_cert=certs[0],
        cert_chain=certs[1:],
        private_key=private_key,
        signature_mechanism=None, # PyHanko lo infiere
    )

    # Crear el escritor de PDF incremental
    w = IncrementalPdfFileWriter(pdf_data)

    # Definir la apariencia de la firma (opcional)
    sig_field_spec = SigFieldSpec(
        sig_field_name='Signature_Profesor_Test', # Nombre genérico para el campo de firma
        box=(50, 50, 250, 150), # Coordenadas de la firma en el PDF (x1, y1, x2, y2)
    )

    # Firmar el PDF
    signed_pdf_data = signers.sign_pdf(
        w,
        sig_field_spec,
        signer,
        # Puedes añadir metadatos adicionales a la firma aquí
        # subfilter=SubFilter.CADES, # Opcional: tipo de subfiltro de firma
        # embed_validation_info=True, # Opcional: incrustar información de validación
        # reason=reason,
        # location=location,
        # doc_mdp_update_policy=DocMDPPerms.NO_CHANGES, # Opcional: política de permisos
    )

    # Guardar el PDF firmado
    with open(output_filepath_str, "wb") as f:
        f.write(signed_pdf_data)

    return Path(output_filepath_str)
