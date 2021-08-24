#!/bin/bash

#echo -n "worksacpe 경로 : "
#read WORKSPACE
#
#WORKSPACE=${WORKSPACE//"~"/"${HOME}"}
#echo ${WORKSPACE}
#
#if [ ! -e ${WORKSPACE} ]; then
#    echo "${WORKSPACE} 가 존재하지 않습니다."
#    exit
#fi
#
#PACKET_GENERATE_TARGET="${WORKSPACE}/vtok_project/data/packet"
#
#if [ ! -d ${PACKET_GENERATE_TARGET} ]; then
#    echo "${PACKET_GENERATE_TARGET} 가 존재하지 않습니다."
#    exit
#fi

PREV_DIR=$(pwd)

SCIRPT_DIR=$(cd "$(dirname $0)"; pwd -P)
SCIRPT_DIR=$(cd "${SCIRPT_DIR}/.."; pwd -P)

#PYTHON3=$(which python3)
#if [ -z ${PYTHON3} ]; then
#    echo $(brew install python3)
#    echo "python3 install complete!"
#fi

ENV_DIR="${SCIRPT_DIR}/.env"
if [ ! -e "${ENV_DIR}" ]; then
    echo $(python3 -m venv ${ENV_DIR})
    echo "python3 enviroment create success"
fi

source "${ENV_DIR}/bin/activate"

pip install -r "${SCIRPT_DIR}/requirements.txt"

deactivate



#PACKET_GENERATE_SOURCE="${SCIRPT_DIR}/commands/packet_generate.sh"
#PACKET_GENERATE_DEST="${PACKET_GENERATE_TARGET}/packet_generate.sh"

#ln -fs ${PACKET_GENERATE_SOURCE} ${PACKET_GENERATE_DEST}

#echo "packet_generate.sh link complete!"

echo "================"
echo "=== Compate! ==="
echo "================"