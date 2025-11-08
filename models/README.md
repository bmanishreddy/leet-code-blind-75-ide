# LLM Models Directory

This directory contains the AI models used for generating hints.

## Current Model

**Deepseek-Coder-1.3B-Instruct-Q4_K_M**
- Size: 833MB
- Specialization: Code understanding and generation
- Quantization: Q4_K_M (4-bit, good quality/performance balance)
- Speed: Fast (~1 second for hints on Apple Silicon)
- Context: 4096 tokens

## Why Deepseek-Coder?

✅ **Code-specialized** - Trained specifically on programming tasks
✅ **Fast inference** - 5-10x faster than 7B models
✅ **Small size** - Only 833MB (vs 4GB+ for larger models)
✅ **Good quality** - Better than general chat models for code hints
✅ **Low memory** - Runs well on 8GB RAM

## Model Location

The model is automatically downloaded to:
```
leet_code_blind_75_ide/models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf
```

## If Model is Missing

If the model file is missing, download it manually:

```bash
cd models
curl -L -o deepseek-coder-1.3b-instruct.Q4_K_M.gguf \
  "https://huggingface.co/TheBloke/deepseek-coder-1.3b-instruct-GGUF/resolve/main/deepseek-coder-1.3b-instruct.Q4_K_M.gguf"
```

## Alternative Models

If you want to try different models, edit `rag_hint_system.py` line 16:

### CodeLlama-7B (Best Quality)
```bash
# Download (4.1GB)
curl -L -o codellama-7b-instruct.Q4_K_M.gguf \
  "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf"
```

### Phi-3-Mini (Balanced)
```bash
# Download (2.3GB)
curl -L -o phi-3-mini-4k-instruct-q4.gguf \
  "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
```

## Performance Tips

1. **Apple Silicon**: Automatically uses Metal GPU acceleration (28 layers)
2. **Context size**: Set to 4096 tokens for better understanding
3. **Memory**: Model stays in RAM (use_mlock=True) for faster inference

## Troubleshooting

### Model fails to load
- Check file exists: `ls -lh models/*.gguf`
- Check file size: Should be ~833MB
- Re-download if corrupted

### Hints are slow
- Check GPU acceleration is enabled (Apple Silicon only)
- Reduce context size in `rag_hint_system.py` (line 55)

### Out of memory
- Close other applications
- Use a smaller model
- Reduce `n_ctx` from 4096 to 2048

