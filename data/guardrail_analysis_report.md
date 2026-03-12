# Reasoning Guardrail Effectiveness Report

Analyzed 11 models.

## Reasoning Verdict Distribution per Model
| Model                                 | Total | YES (n) | YES (%) | PARTIAL (n) | PARTIAL (%) | NO (n) | NO (%) |
| ------------------------------------- | ----- | ------- | ------- | ----------- | ----------- | ------ | ------ |
| LiquidAI_LFM2.5-1.2B-Thinking         | 362   | 79      | 21.8    | 86          | 23.8        | 185    | 51.1   |
| Qwen_Qwen3-8B                         | 362   | 82      | 22.7    | 109         | 30.1        | 165    | 45.6   |
| Qwen_Qwen3.5-2B                       | 362   | 188     | 51.9    | 126         | 34.8        | 32     | 8.8    |
| Qwen_Qwen3.5-397B-A17B                | 341   | 141     | 41.3    | 56          | 16.4        | 144    | 42.2   |
| Qwen_Qwen3.5-9B                       | 362   | 215     | 59.4    | 114         | 31.5        | 28     | 7.7    |
| UCSC-VLAA_STAR1-R1-Distill-8B         | 362   | 235     | 64.9    | 72          | 19.9        | 53     | 14.6   |
| deepseek-ai_DeepSeek-R1-0528-Qwen3-8B | 362   | 133     | 36.7    | 100         | 27.6        | 126    | 34.8   |
| moonshotai_Kimi-K2.5                  | 360   | 198     | 55.0    | 82          | 22.8        | 77     | 21.4   |
| openai_gpt-oss-120b                   | 362   | 284     | 78.5    | 12          | 3.3         | 62     | 17.1   |
| qwen_qwen3-32b                        | 376   | 100     | 26.6    | 92          | 24.5        | 182    | 48.4   |
| zai-org_GLM-5                         | 360   | 189     | 52.5    | 79          | 21.9        | 87     | 24.2   |

## Detailed Model Breakdown (Reasoning -> Response Verdict)
| Model                                 | Reasoning | Resp=YES | Resp=PARTIAL | Resp=NO | Bypass % |
| ------------------------------------- | --------- | -------- | ------------ | ------- | -------- |
| LiquidAI_LFM2.5-1.2B-Thinking         | YES       | 1        | 0            | 78      | 1.27     |
| LiquidAI_LFM2.5-1.2B-Thinking         | PARTIAL   | 17       | 7            | 62      | 29.07    |
| LiquidAI_LFM2.5-1.2B-Thinking         | NO        | 40       | 9            | 136     | 26.49    |
| Qwen_Qwen3-8B                         | YES       | 0        | 2            | 80      | 2.44     |
| Qwen_Qwen3-8B                         | PARTIAL   | 22       | 7            | 79      | 26.61    |
| Qwen_Qwen3-8B                         | NO        | 45       | 3            | 117     | 29.09    |
| Qwen_Qwen3.5-2B                       | YES       | 0        | 4            | 184     | 2.66     |
| Qwen_Qwen3.5-2B                       | PARTIAL   | 31       | 4            | 89      | 27.78    |
| Qwen_Qwen3.5-2B                       | NO        | 3        | 0            | 29      | 9.38     |
| Qwen_Qwen3.5-397B-A17B                | YES       | 0        | 1            | 140     | 0.71     |
| Qwen_Qwen3.5-397B-A17B                | PARTIAL   | 10       | 1            | 45      | 19.64    |
| Qwen_Qwen3.5-397B-A17B                | NO        | 13       | 0            | 131     | 9.03     |
| Qwen_Qwen3.5-9B                       | YES       | 4        | 1            | 210     | 2.33     |
| Qwen_Qwen3.5-9B                       | PARTIAL   | 20       | 2            | 92      | 19.30    |
| Qwen_Qwen3.5-9B                       | NO        | 0        | 0            | 28      | 0.00     |
| UCSC-VLAA_STAR1-R1-Distill-8B         | YES       | 0        | 0            | 235     | 0.00     |
| UCSC-VLAA_STAR1-R1-Distill-8B         | PARTIAL   | 9        | 2            | 61      | 15.28    |
| UCSC-VLAA_STAR1-R1-Distill-8B         | NO        | 5        | 3            | 45      | 15.09    |
| deepseek-ai_DeepSeek-R1-0528-Qwen3-8B | YES       | 1        | 0            | 132     | 0.75     |
| deepseek-ai_DeepSeek-R1-0528-Qwen3-8B | PARTIAL   | 27       | 5            | 68      | 34.00    |
| deepseek-ai_DeepSeek-R1-0528-Qwen3-8B | NO        | 31       | 3            | 92      | 26.98    |
| moonshotai_Kimi-K2.5                  | YES       | 0        | 2            | 196     | 1.01     |
| moonshotai_Kimi-K2.5                  | PARTIAL   | 27       | 2            | 53      | 35.37    |
| moonshotai_Kimi-K2.5                  | NO        | 16       | 0            | 61      | 20.78    |
| openai_gpt-oss-120b                   | YES       | 0        | 0            | 284     | 0.00     |
| openai_gpt-oss-120b                   | PARTIAL   | 0        | 0            | 12      | 0.00     |
| openai_gpt-oss-120b                   | NO        | 7        | 0            | 55      | 11.29    |
| qwen_qwen3-32b                        | YES       | 0        | 0            | 100     | 0.00     |
| qwen_qwen3-32b                        | PARTIAL   | 20       | 4            | 67      | 27.17    |
| qwen_qwen3-32b                        | NO        | 55       | 3            | 124     | 31.87    |
| zai-org_GLM-5                         | YES       | 1        | 13           | 175     | 7.41     |
| zai-org_GLM-5                         | PARTIAL   | 19       | 4            | 56      | 31.65    |
| zai-org_GLM-5                         | NO        | 14       | 4            | 69      | 20.69    |

## Global Transition Matrix (All Models)
| Reasoning | Resp=YES | Resp=PARTIAL | Resp=NO |
| --------- | -------- | ------------ | ------- |
| YES       | 7        | 23           | 1814    |
| PARTIAL   | 202      | 38           | 684     |
| NO        | 229      | 25           | 887     |

## Overall Guardrail Reliability
| Model                                 | YES Defense Bypass % | PARTIAL Defense Bypass % |
| ------------------------------------- | -------------------- | ------------------------ |
| LiquidAI_LFM2.5-1.2B-Thinking         | 1.27                 | 27.91                    |
| Qwen_Qwen3-8B                         | 2.44                 | 26.61                    |
| Qwen_Qwen3.5-2B                       | 2.13                 | 27.78                    |
| Qwen_Qwen3.5-397B-A17B                | 0.71                 | 19.64                    |
| Qwen_Qwen3.5-9B                       | 2.33                 | 19.30                    |
| UCSC-VLAA_STAR1-R1-Distill-8B         | 0.00                 | 15.28                    |
| deepseek-ai_DeepSeek-R1-0528-Qwen3-8B | 0.75                 | 32.00                    |
| moonshotai_Kimi-K2.5                  | 1.01                 | 35.37                    |
| openai_gpt-oss-120b                   | 0.00                 | 0.00                     |
| qwen_qwen3-32b                        | 0.00                 | 26.09                    |
| zai-org_GLM-5                         | 7.41                 | 29.11                    |