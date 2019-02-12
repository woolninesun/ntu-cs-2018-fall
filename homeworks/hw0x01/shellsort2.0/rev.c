int main() {
    buffer = [rbp-2720]
    read( 0, buffer, 0x2710 );

    // sort buffer by byte value, very safely

    rdx = buffer;
    $rsi = 0;
    $rdi = 0;
    $rax = 0;
    call rdx;
}
