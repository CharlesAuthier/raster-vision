from os.path import join

from rastervision.common.data.factory import DataGeneratorFactory
from rastervision.common.utils import _makedirs
from rastervision.tagging.data.planet_kaggle import (
    PLANET_KAGGLE, TIFF, PlanetKaggleTiffFileGenerator)


class TaggingDataGeneratorFactory(DataGeneratorFactory):
    def __init__(self):
        super().__init__([PLANET_KAGGLE], [TIFF])

    def get_class(self, dataset_name, generator_name):
        self.validate_keys(dataset_name, generator_name)
        if dataset_name == PLANET_KAGGLE:
            if generator_name == TIFF:
                return PlanetKaggleTiffFileGenerator

    def plot_generator(self, dataset_name, generator_name, split):
        nb_batches = 2
        batch_size = 4

        class Options():
            def __init__(self):
                self.dataset_name = dataset_name
                self.generator_name = generator_name
                self.active_input_inds = [0, 1, 2, 3]
                self.train_ratio = 0.8
                self.cross_validation = None

        options = Options()
        generator = self.get_data_generator(options)

        viz_path = join(
            self.results_path, 'gen_samples', dataset_name, generator_name,
            split)
        _makedirs(viz_path)

        gen = generator.make_split_generator(
            split, batch_size=batch_size, shuffle=True,
            augment=True, normalize=True, only_xy=False)

        for batch_ind in range(nb_batches):
            batch = next(gen)
            for sample_ind in range(batch_size):
                file_path = join(
                    viz_path, '{}_{}.pdf'.format(batch_ind, sample_ind))
                generator.plot_sample(
                    file_path,
                    batch.all_x[sample_ind, :],
                    batch.y[sample_ind, :],
                    batch.file_inds[sample_ind])


if __name__ == '__main__':
    factory = TaggingDataGeneratorFactory()
    factory.run()
