"""
========================================================================================
UNIVERSIDADE FEEVALE - ENGENHARIA / CIÊNCIA DA COMPUTAÇÃO
DISCIPLINA: SINAIS E SISTEMAS
TÍTULO: UMA ANÁLISE SOBRE FILTROS DIGITAIS UTILIZANDO FERRAMENTAS DE SIMULAÇÃO 
        EM LINGUAGEM PYTHON NO TRATAMENTO DE SINAIS DE ÁUDIO
========================================================================================
ALGORITMO: Separação de Fontes Harmônicas e Percussivas (HPSS - Harmonic-Percussive Source Separation)
MÉTODO: Filtragem Mediana Bidimensional no Domínio Tempo-Frequência (STFT / iSTFT)
ÁUDIO DE TESTE: "Choice" (Admiral Bob) - Bateria e Baixo Elétrico (Creative Commons)
========================================================================================
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def main():
    print("=" * 80)
    print(" ANÁLISE DE FILTROS DIGITAIS NO DOMÍNIO TEMPO-FREQUÊNCIA (HPSS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. CARREGAMENTO E PRÉ-PROCESSAMENTO DO SINAL DE ENTRADA x[n]
    # -------------------------------------------------------------------------
    print("\n[1/5] Carregando sinal de áudio de teste (Bateria + Baixo Elétrico)...")
    caminho_audio = librosa.example('choice')
    y, sr = librosa.load(caminho_audio, sr=22050, mono=True)
    
    duracao = len(y) / sr
    print(f"      -> Taxa de amostragem (Fs): {sr} Hz")
    print(f"      -> Total de amostras (N):   {len(y)}")
    print(f"      -> Duração do sinal:        {duracao:.2f} segundos")

    # -------------------------------------------------------------------------
    # 2. TRANSFORMADA DE FOURIER DE TEMPO CURTO (STFT)
    # -------------------------------------------------------------------------
    # Parâmetros da janela de análise:
    # - n_fft: Tamanho da janela FFT (resolução em frequência)
    # - hop_length: Deslocamento temporal da janela (resolução no tempo)
    print("\n[2/5] Calculando a Transformada de Fourier de Tempo Curto (STFT)...")
    n_fft = 2048
    hop_length = 512
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    print(f"      -> Matriz Espectral D(t, f): {D.shape[0]} bins de frequência x {D.shape[1]} frames temporais")

    # -------------------------------------------------------------------------
    # 3. FILTRAGEM DIGITAL MEDIANA NO ESPECTROGRAMA (HPSS)
    # -------------------------------------------------------------------------
    # O algoritmo aplica dois filtros medianos não-lineares 2D sobre a magnitude:
    # a) Filtro Horizontal (ao longo do tempo): Realça continuidades tonais (Harmônicas)
    # b) Filtro Vertical (ao longo da frequência): Realça transitórios rápidos (Percussivos)
    print("\n[3/5] Aplicando Filtragem Mediana 2D para Separação Harmônica e Percussiva...")
    D_harmonic, D_percussive = librosa.decompose.hpss(D, margin=1.0)

    # -------------------------------------------------------------------------
    # 4. RECONSTRUÇÃO TEMPORAL (iSTFT - Transformada Inversa)
    # -------------------------------------------------------------------------
    print("\n[4/5] Reconstruindo os sinais no domínio do tempo via iSTFT...")
    y_harmonic = librosa.istft(D_harmonic, hop_length=hop_length)
    y_percussive = librosa.istft(D_percussive, hop_length=hop_length)

    # Exportação dos sinais sintetizados para validação auditiva
    sf.write("original.wav", y, sr)
    sf.write("harmonico.wav", y_harmonic, sr)
    sf.write("percussivo.wav", y_percussive, sr)
    print("      -> Arquivos .wav gerados com sucesso:")
    print("         • original.wav    (Sinal de entrada completo)")
    print("         • harmonico.wav   (Componente harmônico filtrado - Contrabaixo)")
    print("         • percussivo.wav  (Componente percussivo filtrado - Bateria)")

    # -------------------------------------------------------------------------
    # 5. ANÁLISE GRÁFICA E ESPECTROGRAMAS COMPARATIVOS
    # -------------------------------------------------------------------------
    print("\n[5/5] Gerando espectrogramas comparativos para análise de sinais...")
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(11, 9), sharex=True)
    fig.suptitle(
        "Separação de Componentes Harmônicos e Percussivos via Filtragem Mediana (STFT)",
        fontsize=13,
        fontweight='bold'
    )

    # Espectrograma 1: Sinal Original
    S_db_orig = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    img0 = librosa.display.specshow(
        S_db_orig, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax[0]
    )
    ax[0].set_title('1. Sinal Original (Mistura Baixo + Bateria)', fontsize=11, fontweight='semibold')
    ax[0].set_ylabel('Frequência (Hz)')
    fig.colorbar(img0, ax=ax[0], format='%+2.0f dB')

    # Espectrograma 2: Componente Harmônico Filtrado
    S_db_harm = librosa.amplitude_to_db(np.abs(D_harmonic), ref=np.max)
    img1 = librosa.display.specshow(
        S_db_harm, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax[1]
    )
    ax[1].set_title('2. Componente Harmônico Filtrado (Filtro Mediano no Eixo do Tempo)', fontsize=11, fontweight='semibold')
    ax[1].set_ylabel('Frequência (Hz)')
    fig.colorbar(img1, ax=ax[1], format='%+2.0f dB')

    # Espectrograma 3: Componente Percussivo Filtrado
    S_db_perc = librosa.amplitude_to_db(np.abs(D_percussive), ref=np.max)
    img2 = librosa.display.specshow(
        S_db_perc, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax[2]
    )
    ax[2].set_title('3. Componente Percussivo Filtrado (Filtro Mediano no Eixo da Frequência)', fontsize=11, fontweight='semibold')
    ax[2].set_xlabel('Tempo (segundos)')
    ax[2].set_ylabel('Frequência (Hz)')
    fig.colorbar(img2, ax=ax[2], format='%+2.0f dB')

    plt.tight_layout()
    nome_grafico = 'resultado_espectrogramas_hpss.png'
    plt.savefig(nome_grafico, dpi=300)
    print(f"      -> Gráfico em alta resolução salvo como: '{nome_grafico}'")
    print("\nProcessamento concluído com sucesso!")
    print("Exibindo espectrogramas...")
    plt.show()


if __name__ == "__main__":
    main()