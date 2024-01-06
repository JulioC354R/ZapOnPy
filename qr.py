import logging
import os
import cv2
from pyzbar.pyzbar import decode
import qrcode


class QR:

    def read_qrcode_img(self, image_path):
        try:
            # Obter o caminho absoluto para a imagem
            image_path = os.path.abspath(image_path)

            qr_code_image = cv2.imread(image_path)

            # Verificar se a imagem foi carregada corretamente
            if qr_code_image is None:
                raise Exception(
                    f"Não foi possível abrir a imagem em: {image_path}")

            # Decodificar o QR code da imagem
            result = decode(qr_code_image)

            # Verificar se algum QR code foi encontrado
            if result:
                # Obter o link (URL) do QR code
                link = str(result[0].data.decode('utf-8'))
                # link = link.replace(',', '')
                logging.info(f'Link encontrado na imagem: {link}')

                # Gerar um novo QR code para o link com uma escala menor
                # Ajuste a escala conforme necessário
                self.qr_code_in_terminal(link, scale=1)
            else:
                logging.info('Nenhum QR code encontrado na imagem.')
        except Exception as e:
            logging.info(f"Erro ao processar a imagem: {e}")

    def qr_code_in_terminal(self, data, scale=1.0):
        # Crie o objeto QRCode com o tamanho desejado
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,  # Ajuste conforme necessário
            border=2,
        )

        # Adicione os dados ao QRCode
        qr.add_data(data)
        qr.make(fit=True)

        # Obtenha a matriz do QRCode
        qr_matrix = qr.get_matrix()

        # Exiba o QRCode no terminal com a escala desejada
        for row in range(0, len(qr_matrix), max(1, int(1/scale))):
            print(''.join('██' if qr_matrix[row][col] else '  ' for col in range(
                0, len(qr_matrix[row]), max(1, int(1/scale)))))
