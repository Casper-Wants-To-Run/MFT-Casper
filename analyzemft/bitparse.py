#!/usr/bin/env python3

# This is all Willi Ballenthin's. Saved me a lot of headaches


# 양수인 경우, 바이트 값 직접 사용
# 음수인 경우, 2의 보수를 이용하여 처리
# 주어진 바이트 배열 -> 리틀 엔디안 형식으로
def parse_little_endian_signed_positive(buf):
    ret = 0
    for i, b in enumerate(buf):
        ret += b * (1 << (i * 8))
    return ret


def parse_little_endian_signed_negative(buf):
    ret = 0
    for i, b in enumerate(buf):
        ret += (b ^ 0xFF) * (1 << (i * 8))
    ret += 1

    ret *= -1
    return ret

# 리틀엔디안 처리
# buf / buf 배열 (마지막 바이트) -> 숫자 변환 후 0b10000000 AND 연산 진행
# 비트가 0인 경우, positive 아닌 경우 negative

def parse_little_endian_signed(buf):
    try:
        if not ord(buf[-1:]) & 0b10000000:
            return parse_little_endian_signed_positive(buf)
        else:
            return parse_little_endian_signed_negative(buf)
    except Exception:
        return ''
