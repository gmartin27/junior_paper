import os
import subprocess
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_file(file, file_name):
    output = Path(args.out) / f"{file_name}.txt"
    print(f"Output: {output}")
    print(f"Input: {file}")

    # skip already done
    if output.exists():
        return(f"Already cleaned {file}")

    subprocess.run([
        "python3",
        "clean.py",
        "--inp", str(file),
        "--out", str(output),
    ])

    return f"Finished cleaning {file}"

def main():
    file_paths = []
    file_names = []

    for f in os.listdir(args.input):
        if os.path.isfile(os.path.join(args.input, f)):
            file_paths.append(os.path.join(args.input, f))
            file_names.append(f.removesuffix(".csv"))

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        for f, fn in zip(file_paths, file_names):
            futures.append(executor.submit(clean_file, f, fn))

        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    output_dir = Path(args.out)
    output_dir.mkdir(exist_ok=True)

    main()
