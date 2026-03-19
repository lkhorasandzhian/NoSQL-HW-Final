import json
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "benchmark/results"


def get_all_files():
    return sorted(
        [f for f in os.listdir(RESULTS_DIR) if f.startswith("benchmark_") and f.endswith(".json")]
    )


def plot_file(filename):
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data["results"]

    test_names = [r["test_name"] for r in results]
    throughput = [r["throughput_ops_sec"] for r in results]

    plt.figure()
    plt.bar(test_names, throughput)

    plt.title(f"Throughput (ops/sec)\n{filename}")
    plt.xlabel("Test Type")
    plt.ylabel("Operations per second")

    plt.xticks(rotation=20)
    plt.tight_layout()

    output_file = os.path.join(
        RESULTS_DIR,
        filename.replace(".json", ".png")
    )

    plt.savefig(output_file)
    plt.close()

    print(f"Chart saved: {output_file}")


def main():
    files = get_all_files()

    if not files:
        print("No benchmark files found.")
        return

    for file in files:
        plot_file(file)

    print("\nAll charts generated successfully.")


if __name__ == "__main__":
    main()