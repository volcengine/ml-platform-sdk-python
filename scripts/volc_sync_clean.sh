#!/usr/bin/env bash

help() {
    echo "Usage:"
    echo "volc_sync.sh -s src_dir -d dst_dir [-i internal_seconds] [-e expire_seconds] "
    echo "Description:"
    echo "  src_dir, required (the path of source directory)"
    echo "  dst_dir, required (the path of destination directory)"
    echo "  internal_seconds, optional, default is 10 (directory synchronization interval)"
    echo "  expire_seconds, optional, default is 0 (when the value is greater than 0, files whose modify time exceeds expire_seconds will be deleted. Please use this option carefully!!!)"
    echo "Example:  nohup bash /root/volc_sync_clean.sh  -s /root/model_ckpt -d /tos_bucket/model_ckpt_path -e 7200  > /root/logs/sync_clean.log 2>&1  &"
    exit -1
}

function get_log_time(){
    local t=$(date +'%Y-%m-%d %H:%M:%S %s%N')
    local t_s=$(echo $t | cut -d " " -f1,2)
    local t_ms=$(echo $t | cut -b30-32)
    echo "${t_s},${t_ms}"
}

function log_info() {
    local msg=$1
    local log_time=$(get_log_time)
	echo -e "${log_time} \033[1;36;40m[INFO]\033[0m $msg"
    return 0
}

function log_warn() {
    local msg=$1
    local log_time=$(get_log_time)
	echo -e "${log_time} \033[1;32;40m[WARN]\033[0m $msg"
    return 1
}

function log_error() {
    local msg=$1
    local log_time=$(get_log_time)
	echo -e "${log_time} \033[1;31;40m[ERROR]\033[0m $msg"
    return 1
}

sync_clean() {
    local src_dir=$1
    local dst_dir=$2
    local internal_seconds=$3
    local expire_seconds=$4

    log_info "successfully started the sync_clean process"

    while true
    do
        log_info "doing sync and clean: src_dir=${src_dir}, dst_dir=${dst_dir}, internal_seconds=${internal_seconds}, expire_seconds=${expire_seconds}"
        rsync -av "$src_dir/" "$dst_dir"
        log_info "finish sync"
        if [[ $expire_seconds -gt 0 ]]; then
            local expire_mins=$((expire_seconds/60+1))
            find ${src_dir} -mmin +${expire_mins} -type f -exec rm -rf {} \;
            log_info "finish clean"
        fi
        sleep "${internal_seconds}s"
    done
}


main() {
    internal_seconds=10
    expire_seconds=0
    daemon=1
    while getopts 's:d:i:e:' OPT; do
        case $OPT in
            s) src_dir="$OPTARG";;
            d) dst_dir="$OPTARG";;
            i) internal_seconds=$OPTARG;;
            e) expire_seconds=$OPTARG;;
            h) help;;
            *) help;;
        esac
    done
    if [ -z "${src_dir}" ] || [ -z "${dst_dir}" ]; then
        help
    else
        sync_clean ${src_dir} ${dst_dir} ${internal_seconds} ${expire_seconds} &
    fi
}


main $@
