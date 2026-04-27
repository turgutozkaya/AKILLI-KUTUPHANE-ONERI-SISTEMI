def get_int_input(prompt):
    """Kullanıcının harf girip programı çökertmesini engeller"""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print(" Hata: Lütfen sadece rakam giriniz!")