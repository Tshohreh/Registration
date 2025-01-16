# -*- coding: utf-8 -*-
"""Registration.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_yEwX4teeuh256yFsjWaldhkcub-UN8h
"""

pip install SimpleITK

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
from google.colab import drive
import os
drive.mount('/content/drive', force_remount=True)

# Load the NIfTI image
nifti_output_path_1 = "/content/drive/My Drive/Datasets/nifti/S_37_T1.nii.gz"
nifti_img = nib.load(nifti_output_path_1)

# Get the data array from the NIfTI image
data = nifti_img.get_fdata()

# Choose a slice to display (e.g., the middle slice along the z-axis)
slice_index = data.shape[-1] // 2

# Plot the slice
plt.imshow(data[:, :, slice_index], cmap='gray')
plt.axis('off')
plt.title('MRI Image')
plt.show()

"""In AI preprocessing, registration refers to the process of aligning or transforming data from different sources or modalities into a common coordinate system or format. This is particularly important in tasks such as image processing, where data may come from different sensors or imaging devices and need to be brought into alignment for accurate analysis or comparison.

For example, in medical imaging, registration may involve aligning MRI and CT scans of the same patient's anatomy to precisely overlay structures for diagnosis or treatment planning. In remote sensing, satellite images taken at different times or from different sensors may need to be registered to track changes in land use or environmental conditions accurately.

Registration algorithms often involve techniques such as feature matching, optimization, or geometric transformations to align the data properly. The goal is to minimize the differences between the data from different sources while preserving relevant information for downstream analysis or machine learning tasks.
"""

fixed_image = sitk.Cast(sitk.ReadImage(nifti_output_path_1), sitk.sitkFloat32)
#moved_image_path = "moved_image.nii"
#moved_image = sitk.Cast(sitk.ReadImage(moved_image_path), sitk.sitkFloat32)

# Define a transformation to move the image
# For example, let's create a translation transformation
translation = sitk.TranslationTransform(3, [10, 20, 30])  # Translate by [10, 20, 30] in x, y, z directions

# Apply the transformation to the fixed image
moved_image = sitk.Resample(fixed_image, translation)

# Save the moved image
sitk.WriteImage(moved_image, 'moved_image.nii')

# Get the data array from the NIfTI image
#sitk.WriteImage(moved_image, 'moved_image.nii.gz')
nifti_moved_image = nib.load('moved_image.nii.gz')
data = nifti_moved_image.get_fdata()

# Choose a slice to display (e.g., the middle slice along the z-axis)
slice_index = data.shape[-1] // 2

# Plot the slice
plt.imshow(data[:, :, slice_index], cmap='gray')
plt.axis('off')
plt.title('Moved MRI Image')
plt.show()

"""import SimpleITK as sitk: Imports the SimpleITK library and assigns it an alias sitk, allowing us to refer to SimpleITK functions and classes using the shorter name sitk.

fixed_image = sitk.ReadImage('fixed_image.nii'): Reads the fixed image from the file named 'fixed_image.nii' using SimpleITK's ReadImage function and assigns it to the variable fixed_image.

moving_image = sitk.ReadImage('moving_image.nii'): Reads the moving image from the file named 'moving_image.nii' using SimpleITK's ReadImage function and assigns it to the variable moving_image.

registration_method = sitk.ImageRegistrationMethod(): Creates an instance of the registration method by calling the ImageRegistrationMethod constructor and assigns it to the variable registration_method.

registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50): Sets the similarity metric to Mattes Mutual Information with 50 histogram bins using the SetMetricAsMattesMutualInformation method of the registration_method.

registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100): Sets the optimizer to Gradient Descent with a learning rate of 1.0 and 100 iterations using the SetOptimizerAsGradientDescent method of the registration_method.

registration_method.SetOptimizerScalesFromPhysicalShift(): Sets the optimizer scales based on the physical shift using the SetOptimizerScalesFromPhysicalShift method of the registration_method.

registration_method.SetInterpolator(sitk.sitkLinear): Sets the interpolator to linear interpolation using the SetInterpolator method of the registration_method.

initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.MOMENTS): Initializes the transformation by finding a transformation that aligns the centers of the fixed and moving images using the CenteredTransformInitializer function and assigns it to the variable initial_transform.

registration_method.SetInitialTransform(initial_transform): Sets the initial transformation for registration using the SetInitialTransform method of the registration_method.

registration_method.SetShrinkFactorsPerLevel([4, 2, 1]): Sets the shrink factors for multi-resolution registration to [4, 2, 1] using the SetShrinkFactorsPerLevel method of the registration_method.

registration_method.SetSmoothingSigmasPerLevel([2, 1, 0]): Sets the smoothing sigmas for multi-resolution registration to [2, 1, 0] using the SetSmoothingSigmasPerLevel method of the registration_method.

registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn(): Specifies that the smoothing sigmas are specified in physical units using the SmoothingSigmasAreSpecifiedInPhysicalUnitsOn method of the registration_method.

final_transform = registration_method.Execute(fixed_image, moving_image): Executes the registration process using the fixed and moving images and assigns the resulting transformation to the variable final_transform.

registered_image = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0): Applies the final transformation to the moving image using linear interpolation and assigns the resulting registered image to the variable registered_image.

sitk.WriteImage(registered_image, 'registered_image.nii'): Writes the registered image to a file named 'registered_image.nii' using SimpleITK's WriteImage function.
"""

# Load the fixed and moving images
#fixed_image = sitk.ReadImage('fixed_image.nii')
#moving_image = sitk.ReadImage('moving_image.nii')
# Choose a registration method
registration_method = sitk.ImageRegistrationMethod()

# Set up the registration
registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
registration_method.SetOptimizerScalesFromPhysicalShift()
registration_method.SetInterpolator(sitk.sitkLinear)

# Set initial transform
initial_transform = sitk.CenteredTransformInitializer(
    fixed_image, moved_image, sitk.Euler3DTransform(),
    sitk.CenteredTransformInitializerFilter.MOMENTS
)
registration_method.SetInitialTransform(initial_transform)

# Set up multi-resolution registration
registration_method.SetShrinkFactorsPerLevel([4, 2, 1])
registration_method.SetSmoothingSigmasPerLevel([2, 1, 0])
registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

# Run the registration
final_transform = registration_method.Execute(fixed_image, moved_image)

# Apply the final transform to the moving image
registered_image = sitk.Resample(moved_image, fixed_image, final_transform, sitk.sitkLinear, 0.0)

# Save the registered image
sitk.WriteImage(registered_image, 'registered_image.nii.gz')

# Get the data array from the NIfTI image
registered_image = nib.load('registered_image.nii.gz')
data = registered_image.get_fdata()

# Choose a slice to display (e.g., the middle slice along the z-axis)
slice_index = data.shape[-1] // 2

# Plot the slice
plt.imshow(data[:, :, slice_index], cmap='gray')
plt.axis('off')
plt.title('Registred MRI Image')
plt.show()