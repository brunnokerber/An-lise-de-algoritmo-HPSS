# Uma Análise sobre Filtros Digitais Utilizando Ferramentas de Simulação em Linguagem Python no Tratamento de Sinais de Áudio

**Universidade Feevale**  
**Disciplina:** Sinais e Sistemas  
**Tema:** Separação de Componentes Harmônicos e Percussivos (HPSS) via Filtragem Mediana no Domínio Tempo-Frequência  

---

## 📌 1. Visão Geral do Projeto

Este projeto tem como objetivo demonstrar e analisar a aplicação de **filtros digitais não-lineares bidimensionais** no processamento de sinais de áudio, utilizando a linguagem **Python** e as bibliotecas científicas `librosa`, `numpy`, `matplotlib` e `soundfile`.

A técnica implementada é o algoritmo **HPSS (*Harmonic-Percussive Source Separation*)**, fundamentado na decomposição de sinais de áudio a partir da **Transformada de Fourier de Tempo Curto (STFT)** e na aplicação de filtros medianos nas direções temporal (horizontal) e frequencial (vertical).

---

## 🔬 2. Fundamentação Teórica e Cadeia de Processamento

A cadeia de processamento implementada em [`projeto.py`](projeto.py) segue o fluxo clássico de Processamento Digital de Sinais (PDS):

```
                       [ Sinal de Entrada x[n] ]
                                  │
                                  ▼
                   [ 1. Amostragem / Janelamento ]
                                  │
                                  ▼
                   [ 2. STFT (Domínio Tempo-Frequência) ]
                                  │
                                  ▼
                   [ 3. Filtragem Mediana Bidimensional ]
                       ┌──────────┴──────────┐
                       ▼                     ▼
             [ Filtro Horizontal ]   [ Filtro Vertical ]
              (Realce Harmônico)     (Realce Percussivo)
                       │                     │
                       ▼                     ▼
             [ Máscara Harmônica ]   [ Máscara Percussiva ]
                       └──────────┬──────────┘
                                  ▼
                   [ 4. iSTFT (Reconstrução Temporal) ]
                       ┌──────────┴──────────┐
                       ▼                     ▼
             [ `harmonico.wav` ]     [ `percussivo.wav` ]
```

### 1. Transformada de Fourier de Tempo Curto (STFT)
Converte o sinal temporal $x[n]$ para uma representação bidimensional $D(t, f)$ no plano tempo-frequência:
* **Tamanho da FFT ($N_{\text{fft}}$):** `2048` amostras (alta resolução em frequência).
* **Deslocamento de Janela (*Hop Length*):** `512` amostras.
* **Taxa de Amostragem ($F_s$):** `22050 Hz`.

### 2. Filtragem Mediana 2D (HPSS)
* **Filtro Horizontal (ao longo do Tempo):** Suprime variações abruptas e preserva cristas de frequência sustentadas no tempo (conteúdo harmônico / melódico, como o contrabaixo).
* **Filtro Vertical (ao longo da Frequência):** Suprime continuidades tonais e preserva pulsos de banda larga instantâneos (transitórios percussivos, como bumbo, caixa e pratos).

### 3. Reconstrução Temporal (iSTFT)
Aplica a Transformada Inversa com sobreposição e soma (*Overlap-Add*) para recuperar as formas de onda no domínio do tempo para audição e validação.

---

## 📁 3. Estrutura do Diretório

```plaintext
Análise de algoritmo HPSS/
├── projeto.py                     # Script principal em Python
├── README.md                      # Documentação técnica do projeto
├── original.wav                   # Áudio de entrada original (Mix completo)
├── harmonico.wav                  # Componente harmônico isolado (Contrabaixo)
├── percussivo.wav                 # Componente percussivo isolado (Bateria)
└── resultado_espectrogramas_hpss.png # Gráfico comparativo dos espectrogramas (300 DPI)
```

---

## 🚀 4. Pré-requisitos e Instalação

Certifique-se de possuir o **Python 3.10+** instalado. Em seguida, instale as dependências necessárias executando no terminal:

```bash
pip install librosa matplotlib numpy soundfile
```

---

## 💻 5. Como Executar

Abra o terminal dentro desta pasta e execute:

```bash
python projeto.py
```

### Resultados da Execução:
1. **No Terminal:** Serão exibidos os logs de cada etapa com dados quantitativos ($F_s$, número de amostras, dimensões da matriz STFT).
2. **Arquivos de Áudio:** Serão salvos/atualizados os arquivos `original.wav`, `harmonico.wav` e `percussivo.wav` para comparação auditiva.
3. **Figura Gráfica:** Será gerada a imagem `resultado_espectrogramas_hpss.png` em alta definição contendo os 3 espectrogramas alinhados temporalmente e a janela de visualização do `matplotlib`.

---

## 📊 6. Interpretação dos Resultados

* **Espectrograma 1 (Original):** Demonstra a sobreposição completa de linhas horizontais densas nos graves (baixo) e listras verticais periódicas (batidas da bateria).
* **Espectrograma 2 (Harmônico):** Mostra a remoção quase completa dos transitórios verticais, restando as linhas contínuas das notas do baixo.
* **Espectrograma 3 (Percussivo):** Mostra a atenuação das notas contínuas, mantendo apenas as bandas de energia vertical dos ataques percussivos.

---

## 📜 7. Referências e Áudio de Teste
* **Áudio Utilizado:** *"Choice"* (Admiral Bob) - Bateria e Contrabaixo (Licença Creative Commons CC-BY).
* **Biblioteca:** [librosa: Audio and Music Signal Analysis in Python](https://librosa.org/)
* **Algoritmo Base:** Fitzgerald, D. (2010). *Harmonic/percussive separation using median filtering*. 13th International Conference on Digital Audio Effects (DAFx10).
