import glob
import os.path as osp
import multiresolutionimageinterface as mir

slide_path = r'D:\camelyon\images'
anno_path = r'D:\camelyon\annotations'
mask_path = r'D:\camelyon\masks'

# Get all .tif files and filter for tumor images only
tumor_paths = glob.glob(osp.join(slide_path, 'tumor_*.tif'))
tumor_paths.sort()

# Get all annotation files and sort
anno_tumor_paths = glob.glob(osp.join(anno_path, '*.xml'))
anno_tumor_paths.sort()

# Create a dictionary to map base names to annotation paths
anno_dict = {osp.basename(path).replace('.xml', ''): path for path in anno_tumor_paths}

reader = mir.MultiResolutionImageReader()

for tumor_path in tumor_paths:
    base_name = osp.basename(tumor_path).replace('.tif', '')
    if base_name in anno_dict:
        print(f"Processing {tumor_path} with annotation {anno_dict[base_name]}")

        # Verify the content of the XML file
        xml_file_path = anno_dict[base_name]
        with open(xml_file_path, 'r') as file:
            xml_content = file.read()
            print(f"Contents of {xml_file_path}:\n{xml_content}")

        mr_image = reader.open(tumor_path)
        annotation_list = mir.AnnotationList()
        print(f"Initial number of annotations: {len(annotation_list.getAnnotations())}")

        xml_repository = mir.XmlRepository(annotation_list)
        xml_repository.setSource(anno_dict[base_name])

        try:
            xml_repository.load()
            print(f"Number of annotations after loading: {len(annotation_list.getAnnotations())}")
        except Exception as e:
            print(f"Error loading annotations from {anno_dict[base_name]}: {e}")
            continue

        if len(annotation_list.getAnnotations()) == 0:
            print(f"No annotations found in {anno_dict[base_name]}")
            continue

        for annotation in annotation_list.getAnnotations():
            print(
                f"Annotation: {annotation.getName()}, Type: {annotation.getType()}")

        annotation_mask = mir.AnnotationToMask()

        label_map = {'Tumor': 255}
        conversion_order = ['Tumor']

        print(f"Generating mask for {tumor_path}")
        output_path = osp.join(mask_path, osp.basename(tumor_path).replace('.tif', '_mask.tif'))
        print(f"Output path: {output_path}")
        print(f"Image dimensions: {mr_image.getDimensions()}")
        print(f"Image spacing: {mr_image.getSpacing()}")

        annotation_mask.convert(annotation_list, output_path, mr_image.getDimensions(), mr_image.getSpacing(),
                                label_map, conversion_order)
    else:
        print(f"No annotation file found for {tumor_path}")