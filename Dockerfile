# 1. Usamos la imagen oficial de AWS Lambda para Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# 2. Copiamos los requerimientos
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# 3. Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos TODA tu carpeta src manteniendo su estructura interna intacta
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# 5. ¡El cambio maestro! Le decimos a Lambda la ruta exacta en formato de módulo Python
# Ruta del archivo: src/infra/adapters/inbound/main.py
# Variable adentro: handler
CMD [ "src.infra.adapters.inbound.main.handler" ]