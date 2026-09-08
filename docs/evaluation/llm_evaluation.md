# LLM Evaluation

## 1. Motivation

The initial implementation used `Qwen/Qwen2.5-7B-Instruct` as the LLM.

During API testing, the model occasionally produced abnormal outputs, including:

- corrupted or unexpected characters
- repeated tokens
- simulated conversation roles
- incomplete or low-quality responses

Because the issue could have originated from different layers of the application, the LLM was tested independently from the database, API and service layers.

---

## 2. Debugging Process

The debugging process followed an isolation-based approach:

1. Tested the complete message API.
2. Identified abnormal LLM responses.
3. Created a standalone LLM test to bypass the database and service layer.
4. Tested different system prompts.
5. Tested both Chinese and English prompts.
6. Compared different temperature settings.
7. Tested multiple candidate LLMs using the same benchmark setup.

This helped determine that the issue was not caused by the database or FastAPI message workflow.

---

## 3. Model Benchmark

The following models were evaluated:

- `Qwen/Qwen2.5-7B-Instruct`
- `deepseek-ai/DeepSeek-V3.2`
- `Qwen/Qwen3-32B`
- `zai-org/GLM-5.2`
- `deepseek-ai/DeepSeek-V4-Flash`

The models were evaluated using the same:

- system prompt
- user queries
- temperature
- generation configuration

### Evaluation Criteria

| Criterion | Description |
|---|---|
| Instruction Following | Follows the technical support instructions |
| Chinese Quality | Natural and clear Chinese responses |
| Stability | Absence of malformed or unexpected output |
| Completeness | Response reaches a natural conclusion |
| Technical Usefulness | Provides actionable troubleshooting steps |

---

## 4. Results

### Qwen2.5-7B-Instruct

The model frequently produced abnormal output during direct testing.

Example symptoms included malformed characters, repeated tokens and unexpected role-like text.

Conclusion:

**Not selected.**

---

### DeepSeek-V3.2

DeepSeek-V3.2 produced consistently coherent technical support responses.

Strengths:

- stable output
- good Chinese quality
- clear troubleshooting structure
- actionable technical suggestions
- appropriate follow-up questions
- no observed role contamination

Conclusion:

**Selected as the current primary LLM.**

---

### Qwen3-32B

Qwen3-32B produced technically detailed and high-quality responses.

It performed particularly well when providing concrete troubleshooting commands and infrastructure-level checks.

However, the responses tended to be more detailed than necessary for a first-line technical support assistant.

Conclusion:

**Strong alternative candidate.**

---

### GLM-5.2

GLM-5.2 produced high-quality Chinese technical support responses and showed good ability to identify relevant diagnostic information.

However, responses frequently reached the configured token limit before naturally completing.

Conclusion:

**Not selected under the current generation configuration.**

---

### DeepSeek-V4-Flash

DeepSeek-V4-Flash also produced technically useful and structured responses.

However, several responses reached the configured token limit before completion.

Conclusion:

**Not selected for the current implementation.**

---

## 5. Model Selection

Based on the current benchmark, `deepseek-ai/DeepSeek-V3.2` was selected as the primary LLM.

The priority for this project is:

1. Stability
2. Instruction following
3. Chinese response quality
4. Technical usefulness
5. Cost and latency

The model configuration is currently:

```text
Model: deepseek-ai/DeepSeek-V3.2
Temperature: 0.2
Max tokens: 300