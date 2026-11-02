# Hyperparameter sweep

Baseline: living_reward=-0.04, gamma=0.9, alpha=0.5, epsilon=0.1. 500 episodes, 10 seeds per setting. One value changes at a time.

## living_reward

| value | goal% | policy% | first optimal episode | avg return (last 50) |
|---|---|---|---|---|
| 0.0 | 100 | 79 | 11 | 9.78 |
| -0.04 **(chosen)** | 100 | 93 | 11 | 9.58 |
| -0.5 | 100 | 94 | 12 | 7.04 |
| -2.0 | 100 | 79 | 16 | -1.28 |
| -5.0 | 0 | 95 | 256 | -17.66 |

## gamma

| value | goal% | policy% | first optimal episode | avg return (last 50) |
|---|---|---|---|---|
| 0.5 | 100 | 94 | 10 | 9.54 |
| 0.9 **(chosen)** | 100 | 93 | 11 | 9.58 |
| 0.99 | 100 | 91 | 10 | 9.51 |
| 1.0 | 100 | 87 | 10 | 9.51 |

## alpha

| value | goal% | policy% | first optimal episode | avg return (last 50) |
|---|---|---|---|---|
| 0.1 | 100 | 93 | 15 | 9.56 |
| 0.5 **(chosen)** | 100 | 93 | 11 | 9.58 |
| 0.9 | 100 | 92 | 10 | 9.43 |

## epsilon

| value | goal% | policy% | first optimal episode | avg return (last 50) |
|---|---|---|---|---|
| 0.01 | 100 | 88 | 10 | 9.80 |
| 0.1 **(chosen)** | 100 | 93 | 11 | 9.58 |
| 0.3 | 100 | 95 | 11 | 8.80 |
| 0.5 | 100 | 100 | 10 | 8.23 |

