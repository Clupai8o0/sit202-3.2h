from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_cert(cert_name_prefix="server"):
  # 1. Generate a private key
  private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
  )

  # 2. Generating public key from private key
  public_key = private_key.public_key()

  # 3. Generate certificate using X509
  subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")
  ])
  # Generating a different Certificate Name for client
  if cert_name_prefix == "client":
    subject = issuer = x509.Name([
      x509.NameAttribute(NameOID.COMMON_NAME, u"client.localhost"),
    ])
  
  # 4. Build the certificate
  cert = x509.CertificateBuilder().subject_name(subject
  ).issuer_name(issuer
  ).public_key(public_key
  ).serial_number(x509.random_serial_number()
  ).not_valid_before(datetime.now(timezone.utc)
  ).not_valid_after(datetime.now(timezone.utc) + timedelta(days=365)
  ).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
  ).sign(private_key, hashes.SHA256())

  # 5. Save the certificate and private keys
  # Save the private key
  with open(f"{cert_name_prefix}.key", "wb") as f:
    f.write(private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
    ))
  # Save the certificate
  with open(f"{cert_name_prefix}.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

  # print success output
  print(f"Generate {cert_name_prefix}.key and {cert_name_prefix}.crt successfully")

if __name__ == "__main__":
  generate_cert("server")
  generate_cert("client")