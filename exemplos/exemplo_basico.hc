int x;
bool positivo;

x = read();
positivo = x > 0;

if (positivo) {
    print(x);
} else {
    print(0);
}

while (x > 0) {
    x = x - 1;
}
