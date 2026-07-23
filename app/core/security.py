import bcrypt

def hash_password(password: str) -> str:
    #implementação de hashing de senha (exemplo simples, não seguro para produçao)
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    #implementação de verificação de senha.
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))