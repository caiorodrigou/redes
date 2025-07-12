#include <iostream>
#include <cmath>
#include <string>
#include <algorithm>

using namespace std;

long long karatsuba(long long u, long long v,long long n) {;
    // se n for menor ou igual a 3,
    // não é necessario usar o katatsuba, já retorna a multiplicação
    if (n <= 3)
        return u * v;

    // Calcular m
    int m = n / 2;

    // Dividir u em p e q
    long long p = u / static_cast<long long>(pow(10, m));
    long long q = u % static_cast<long long>(pow(10, m));

    // Dividir v em r e s
    long long r = v / static_cast<long long>(pow(10, m));
    long long s = v % static_cast<long long>(pow(10, m));

    // Passos 8, 9 e 10: Calcula pr, qs e y
    long long pr = karatsuba(p, r, m);
    long long qs = karatsuba(q, s, m);
    long long y = karatsuba(p + q, r + s, m);

    // Passo 11: Calcula o resultado final
    long long uv = pr * static_cast<long long>(pow(10, 2 * m)) + (y - pr - qs) * static_cast<long long>(pow(10, m)) + qs;

    return uv;
}

int main() {
    long long u, v, n;
    cout << "Digite o primeiro número: ";
    cin >> u;
    cout << "Digite o segundo número: ";
    cin >> v;
    cout << "Digite o tamanho dos números: ";
    cin >> n;   

    long long resultado = karatsuba(u, v, n);
    cout << "Resultado: " << resultado << endl;

    return 0;
}
