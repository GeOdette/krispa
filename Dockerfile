FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/wf-base:fbe8-main

#Install conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
# Install dependencies 
RUN conda install -c bioconda parallel-fastq-dump &&\
    conda install -c bioconda blast &&\
    conda install -c kantorlab blastn

# Install CRISPRbuilder-TB
RUN pip install crisprbuilder_tb

#Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY wf /root/wf

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio
