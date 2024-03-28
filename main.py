import usb.core
import usb.util

# Знайдіть CP2112 пристрій за vendor ID і product ID
vendor_id = 0x10C4  # Silicon Labs
product_id = 0xEA90  # CP2112
device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

if device is None:
    raise ValueError('CP2112 device not found')
else:
    print('Device found')

# Встановлення конфігурації, якщо потрібно
device.set_configuration()

# Функція для запису даних на I2C пристрій
endpoint_write = 0x01


def write_i2c_data(address, data):
    report = [0x00]  # Report ID для I2C запису
    report.append(address << 1)
    report.extend(data)
    device.write(endpoint_write, report)


# Для читання, вам потрібно також визначити кінцеву точку читання, припустимо, це 0x81
endpoint_read = 0x81


def read_i2c_data(address, count):
    report = [0x01]
    report.append(address << 1 | 0x01)
    report.append(count)
    device.write(endpoint_write, report)
    data = device.read(endpoint_read, count + 1)

    return data[1:]  # Повертаємо дані без report ID


# Приклад використання
# write_i2c_data(0x50, [0x00, 0x01, 0x02])
if __name__ == '__main__':
    for addr in range(128):
        read_data = read_i2c_data(addr, 1)
        print(read_data)
