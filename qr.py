import os
import cv2
from pyzbar.pyzbar import decode
import qrcode


class QR:

    def ler_qrcode_imagem(self, nome_da_imagem):
        try:
            # Obter o caminho absoluto para a imagem
            caminho_da_imagem = os.path.abspath(
                os.path.join(os.getcwd(), nome_da_imagem))

            # Carregar a imagem
            imagem = cv2.imread(caminho_da_imagem)

            # Verificar se a imagem foi carregada corretamente
            if imagem is None:
                raise Exception(
                    f"Não foi possível abrir a imagem em: {caminho_da_imagem}")

            # Decodificar o QR code da imagem
            resultado = decode(imagem)

            # Verificar se algum QR code foi encontrado
            if resultado:
                # Obter o link (URL) do QR code
                link = str(resultado[0].data.decode('utf-8'))
                # link = link.replace(',', '')
                print(f'Link encontrado na imagem: {link}')

                # Gerar um novo QR code para o link com uma escala menor
                # Ajuste a escala conforme necessário
                self.gerar_qrcode_terminal(link, escala=1)
            else:
                print('Nenhum QR code encontrado na imagem.')
        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")

    def gerar_qrcode_terminal(self, dados, escala=1.0):
        # Crie o objeto QRCode com o tamanho desejado
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,  # Ajuste conforme necessário
            border=2,
        )

        # Adicione os dados ao QRCode
        qr.add_data(dados)
        qr.make(fit=True)

        # Obtenha a matriz do QRCode
        qr_matrix = qr.get_matrix()

        # Exiba o QRCode no terminal com a escala desejada
        for row in range(0, len(qr_matrix), max(1, int(1/escala))):
            print(''.join('██' if qr_matrix[row][col] else '  ' for col in range(
                0, len(qr_matrix[row]), max(1, int(1/escala)))))
