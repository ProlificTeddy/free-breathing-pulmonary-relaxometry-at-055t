# Free-breathing Pulmonary Relaxometry at 0.55T

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/release/python-380/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Paper](https://img.shields.io/badge/ArXiv-2607.02200v1-orange)](https://arxiv.org/pdf/2607.02200v1)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](https://github.com/your-repo-link)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Overview

This repository contains the Python implementation of the research paper **[Free-breathing Pulmonary Relaxometry at 0.55T](https://arxiv.org/pdf/2607.02200v1)** by Pavlos Panos et al. The paper introduces a novel, fully automated workflow for free-breathing 2D pulmonary relaxometry (T1 and T2 mapping) at 0.55T. 

The proposed method eliminates the need for breath-holds or external gating, making it a patient-friendly solution for quantitative lung MRI. The pipeline integrates:
- A 2D inversion recovery ultra-fast balanced steady-state free precession (IR-uf-bSSFP) sequence for high-temporal sampling.
- Multi-contrast registration for motion correction.
- Deep learning-based lung segmentation.
- Voxel-wise nonlinear fitting for T1 and T2 map generation.

This repository provides an implementation of the methodology described in the paper, enabling researchers and clinicians to reproduce the results and explore the potential of free-breathing pulmonary relaxometry in their own studies.

---

## How It Works

The pipeline consists of the following key steps:

1. **Data Acquisition**:
   - A 2D IR-uf-bSSFP sequence is adapted to acquire images at 0.55T. This sequence captures the transient phase with high temporal resolution, allowing for accurate T1 and T2 relaxometry.

2. **Motion Correction**:
   - Multi-contrast registration is applied to correct for respiratory motion during free-breathing. This ensures that voxel-wise analysis is not affected by misalignment.

3. **Lung Segmentation**:
   - A deep learning-based model is used to segment the lung parenchyma from the acquired images. This step isolates the region of interest for relaxometry analysis.

4. **Relaxation Mapping**:
   - Voxel-wise nonlinear fitting is performed to generate quantitative T1 and T2 maps. These maps provide insights into the relaxation properties of lung tissue.

5. **Validation**:
   - The pipeline is validated using phantom experiments and tested on in-vivo data from healthy volunteers and a patient with a lung lesion. The results demonstrate the accuracy and clinical relevance of the method.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-link/free-breathing-relaxometry.git
   cd free-breathing-relaxometry
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install a GPU-compatible version of PyTorch for faster deep learning-based segmentation:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

---

## Usage

### Running the Implementation

The main script for the pipeline is `implementation.py`. It takes raw MRI data as input and outputs T1 and T2 maps. Here's how to use it:

1. Prepare your input data:
   - Ensure your MRI data is in NIfTI format (`.nii` or `.nii.gz`).
   - Organize your data into the following folder structure:
     ```
     data/
     ├── subject_01/
     │   ├── raw_image.nii
     │   └── mask.nii (optional, for custom lung segmentation)
     ├── subject_02/
     │   ├── raw_image.nii
     │   └── mask.nii
     ```

2. Run the pipeline:
   ```bash
   python implementation.py --data_dir data/ --output_dir results/
   ```

   - `--data_dir`: Path to the folder containing input data.
   - `--output_dir`: Path to the folder where results will be saved.

3. View the results:
   - The pipeline will generate T1 and T2 maps for each subject in the `results/` directory. These maps will be saved as `.nii.gz` files.

### Example Command

```bash
python implementation.py --data_dir ./example_data --output_dir ./output_results
```

---

## Results

The pipeline outputs the following for each subject:
- **T1 Map**: A quantitative map of T1 relaxation times (in milliseconds).
- **T2 Map**: A quantitative map of T2 relaxation times (in milliseconds).

Example visualization of the results:

| Input Image | T1 Map | T2 Map |
|-------------|--------|--------|
| ![Input](images/input_image.png) | ![T1](images/t1_map.png) | ![T2](images/t2_map.png) |

---

## Repository Structure

```
free-breathing-relaxometry/
├── data/                   # Example input data
├── results/                # Output directory for results
├── models/                 # Pre-trained deep learning models for lung segmentation
├── utils/                  # Utility scripts for preprocessing and visualization
├── implementation.py       # Main script for running the pipeline
├── requirements.txt        # Python dependencies
├── LICENSE                 # License information
└── README.md               # Project documentation
```

---

## Citation

If you use this code or find it helpful in your research, please cite the original paper:

```
@article{panos2023freebreathing,
  title={Free-breathing Pulmonary Relaxometry at 0.55T},
  author={Pavlos Panos, Oliver Bieri, Maurice Pradella, Katrin E. Hostettler, Grzegorz Bauman},
  journal={arXiv preprint arXiv:2607.02200v1},
  year={2023}
}
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss your ideas.

---

## Acknowledgments

We thank the authors of the paper for their groundbreaking work and for making the research publicly available. This implementation is inspired by their methodology and aims to make the proposed workflow accessible to the wider research community.

--- 

Happy coding! 🚀