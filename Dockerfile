FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/wf-base:fbe8-main

# Clone the directory
RUN git clone https://github.com/cguyeux/CRISPRbuilder-TB.git

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
