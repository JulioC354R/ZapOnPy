import random
class Bot:
    """Essa classe é responsável por realizar outras funções do bot ligadas ao RPG, como autenticação de ADMs e calculos"""
    
    def __init__(self) -> None:
        self.adms_numbers = [] #["+55 18 98800-3813", "+55 81 9605-2190"]

    def is_adm(self, number):
        if number not in self.adms_numbers:
            return True
        else:
            return False
    
    
    def calcular_acerto(precisao_personagem, precisao_distancia):
        """Calcula o acerto de um projétil com base na precisão do personagem e na precisão baseada na distância.

        Args:
            precisao_personagem: A precisão do personagem, em porcentagem.
            precisao_distancia: A precisão baseada na distância, em porcentagem.

        Returns:
            Uma porcentagem que representa a probabilidade de acerto do projétil.
            Também retorna as chances de todos os 10 tiros errarem.
        """

        if precisao_distancia < 0 or precisao_distancia > 100:
            raise ValueError("A precisão baseada na distância deve estar entre 0 e 100.")

        taxa_acerto = (precisao_personagem + precisao_distancia) / 2
        chances_de_erro = 100 - taxa_acerto

        # Arredonda a taxa de acerto e as chances de erro para o inteiro mais próximo.

        tiros_acertados = 0
        tiros_errados = 0
        for _ in range(10):
            if random.randint(0, 100) <= taxa_acerto:
                tiros_acertados += 1
            else:
                tiros_errados += 1
        probabilidade_errar_tudo = (chances_de_erro / 100) ** 10
        return taxa_acerto, chances_de_erro, tiros_acertados, tiros_errados, probabilidade_errar_tudo

        t, c, a, e, probabilidade_errar_tudo = calcular_acerto(50, 90)
        print(f'taxa de acerto = {t:.2f}%\nchance de erro = {c:.2f}\nacertou = {a}\nerrou = {e}\nchances de errar tudo = {probabilidade_errar_tudo:.14f}')

    
    

