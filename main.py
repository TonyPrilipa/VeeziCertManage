def cert_separate(certificate):
    certificate = certificate[1:-1]   # remove '(' and ')'
    serial_num = certificate[:4]    # serial num certificate group
    cert_num = certificate[4:]      # num of cert in group
    return int(serial_num), int(cert_num)


while True:
    input_cert = input('Waiting for certificate: ')

    serial, cert = cert_separate(input_cert)

    print(serial, cert)
