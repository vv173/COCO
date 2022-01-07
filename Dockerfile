FROM python:3.8.10-slim-buster

RUN useradd -m coco
USER coco
WORKDIR /home/coco/

COPY --chown=coco:coco requirements.txt .
COPY --chown=coco:coco COCO.py .
COPY --chown=coco:coco start.sh .

RUN chmod +x ./COCO.py && \
    chmod +x ./start.sh && \
    mkdir /home/coco/wheelhouse && \
    mkdir /home/coco/data

COPY ./wheelhouse/* /home/coco/wheelhouse/

RUN pip install --upgrade pip && \
    pip install --upgrade wheel && \
    pip install --upgrade setuptools && \
    pip install --upgrade Cython && \
    pip install -r requirements.txt \
        --no-index --find-links /home/coco/wheelhouse/

CMD python COCO.py -p $COCO_PATH -u $URL