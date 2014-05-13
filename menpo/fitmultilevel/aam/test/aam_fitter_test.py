import numpy as np
from numpy.testing import assert_allclose
from nose.tools import raises

import menpo.io as mio
from menpo.shape.pointcloud import PointCloud
from menpo.landmark import labeller, ibug_68_trimesh
from menpo.transform import PiecewiseAffine
from menpo.fitmultilevel.aam import AAMBuilder
from menpo.fitmultilevel.aam import LucasKanadeAAMFitter
from menpo.fit.lucaskanade.appearance import AlternatingForwardAdditive, \
    AlternatingForwardCompositional, AlternatingInverseCompositional, \
    AdaptiveForwardAdditive, AdaptiveForwardCompositional, \
    AdaptiveInverseCompositional, SimultaneousForwardAdditive, \
    SimultaneousForwardCompositional, SimultaneousInverseCompositional, \
    ProjectOutForwardAdditive, ProjectOutForwardCompositional, \
    ProjectOutInverseCompositional, ProbabilisticForwardAdditive, \
    ProbabilisticForwardCompositional, ProbabilisticInverseCompositional

initial_shape = []
initial_shape.append(PointCloud(np.array([[169.99818621, 42.1538478],
                                       [201.66315932, 44.1290254],
                                       [242.7854523, 51.89297215],
                                       [281.90562277, 64.43830484],
                                       [316.58752267, 74.82329741],
                                       [348.0100063, 93.92053445],
                                       [373.88213144, 112.22764684],
                                       [405.03132538, 133.66232212],
                                       [413.8021522, 168.09483526],
                                       [406.51514226, 207.67276427],
                                       [387.97333922, 253.02170949],
                                       [355.91753642, 292.42364566],
                                       [308.37911044, 346.44865143],
                                       [253.62011094, 371.27657762],
                                       [193.2988118, 376.70750725],
                                       [130.92094517, 371.15479632],
                                       [71.14761525, 354.34070763],
                                       [113.79199586, 35.05614932],
                                       [101.87689909, 47.16339582],
                                       [94.99286454, 64.03792851],
                                       [94.50621858, 82.8716246],
                                       [99.5172678, 99.33158965],
                                       [89.65977368, 120.63168136],
                                       [63.43821987, 146.60324958],
                                       [46.14888693, 178.20941269],
                                       [43.56132947, 213.74288177],
                                       [61.84397722, 249.7861648],
                                       [122.42885278, 112.45080876],
                                       [149.80686246, 107.69095186],
                                       [179.56175158, 104.00323278],
                                       [211.65442703, 100.14000505],
                                       [233.08284923, 81.89258936],
                                       [242.38644685, 106.00171695],
                                       [245.1757708, 130.94304409],
                                       [238.80506153, 148.3025409],
                                       [232.44269795, 164.44249341],
                                       [150.32251956, 63.76477162],
                                       [136.44759869, 71.43400903],
                                       [132.8319703, 88.80641534],
                                       [135.0308641, 102.88772426],
                                       [145.22040924, 91.97623707],
                                       [153.31004671, 76.17059151],
                                       [126.66484876, 162.9615981],
                                       [100.48243755, 176.43886212],
                                       [93.11827984, 197.6627901],
                                       [99.54588384, 222.37450015],
                                       [111.53888228, 204.50007046],
                                       [120.59523853, 183.5325519],
                                       [308.09891852, 114.8721147],
                                       [294.96662988, 119.58754591],
                                       [288.08786026, 127.93478303],
                                       [289.23424405, 145.12627472],
                                       [282.41722002, 159.25200354],
                                       [284.79324576, 188.78643868],
                                       [290.88156244, 221.13819024],
                                       [308.73120003, 190.27433932],
                                       [316.0602659, 164.32754423],
                                       [318.39022041, 147.62671215],
                                       [319.59091967, 133.47904846],
                                       [317.15479142, 122.0301549],
                                       [306.30903709, 120.60649663],
                                       [302.1938359, 133.03875418],
                                       [296.14415784, 145.2469796],
                                       [292.66657074, 160.06350712],
                                       [291.24846445, 209.46777536],
                                       [301.33163129, 160.69858648],
                                       [305.1779705, 145.84067693],
                                       [306.9300967, 131.15196026]])))

initial_shape.append(PointCloud(np.array([[132.35794195, 69.2578397],
                                       [162.38175839, 71.13064627],
                                       [201.37273342, 78.49219719],
                                       [238.46535349, 90.3873207],
                                       [271.3497331, 100.23407185],
                                       [301.14362799, 118.34152255],
                                       [325.67483265, 135.69979978],
                                       [355.20960212, 156.02354217],
                                       [363.52584776, 188.67146043],
                                       [356.61651459, 226.19811397],
                                       [339.03571043, 269.19667904],
                                       [308.64132054, 306.55646125],
                                       [263.5667528, 357.78141731],
                                       [211.645845, 381.32254256],
                                       [154.45092472, 386.47199378],
                                       [95.30602633, 381.20707304],
                                       [38.63067471, 365.26443792],
                                       [79.06484943, 62.52800622],
                                       [67.76729749, 74.007749],
                                       [61.240054, 90.00769538],
                                       [60.77863031, 107.86526413],
                                       [65.529963, 123.4721294],
                                       [56.18337069, 143.66826351],
                                       [31.32084782, 168.29375724],
                                       [14.92759978, 198.26181173],
                                       [12.47415224, 231.95362474],
                                       [29.80923281, 266.12882867],
                                       [87.25406866, 135.91139549],
                                       [113.21310972, 131.39823614],
                                       [141.42583947, 127.90164701],
                                       [171.85519096, 124.23864562],
                                       [192.17300435, 106.93697108],
                                       [200.99440793, 129.79655219],
                                       [203.63916464, 153.44520097],
                                       [197.59864141, 169.90497638],
                                       [191.56603133, 185.20841497],
                                       [113.70204094, 89.74869588],
                                       [100.54624019, 97.02044613],
                                       [97.11800537, 113.49246195],
                                       [99.20293321, 126.84395392],
                                       [108.86436674, 116.49799572],
                                       [116.53472823, 101.51153736],
                                       [91.27051817, 183.80427265],
                                       [66.44510918, 196.58302662],
                                       [59.46262673, 216.70694447],
                                       [65.55709591, 240.13787694],
                                       [76.92851196, 223.18985699],
                                       [85.51548839, 203.30905917],
                                       [263.30108288, 138.20720812],
                                       [250.84942464, 142.67824432],
                                       [244.3271732, 150.59285439],
                                       [245.41414133, 166.89333217],
                                       [238.95043528, 180.28694181],
                                       [241.20331452, 208.29064345],
                                       [246.97608123, 238.96564345],
                                       [263.90059402, 209.70142802],
                                       [270.8498034, 185.09942346],
                                       [273.05899923, 169.264175],
                                       [274.19746772, 155.84976735],
                                       [271.88760101, 144.99425589],
                                       [261.6039688, 143.64438408],
                                       [257.70205344, 155.43229298],
                                       [251.96592277, 167.00778107],
                                       [248.66857474, 181.05638616],
                                       [247.32396715, 227.90009184],
                                       [256.88453583, 181.65855014],
                                       [260.53152401, 167.5707078],
                                       [262.19283966, 153.64328928]])))

# load images
filenames = ['breakingbad.jpg', 'einstein.jpg']
training_images = []
for i in range(2):
    im = mio.import_builtin_asset(filenames[i])
    im.crop_to_landmarks_proportion(0.1)
    labeller(im, 'PTS', ibug_68_trimesh)
    if im.n_channels == 3:
        im = im.as_greyscale(mode='luminosity')
    training_images.append(im)

# build aam
aam = AAMBuilder(feature_type=['igo', 'igo', None],
                 transform=PiecewiseAffine,
                 trilist=training_images[0].landmarks['ibug_68_trimesh'].
                 lms.trilist,
                 normalization_diagonal=150,
                 n_levels=3,
                 downscale=2,
                 scaled_shape_models=False,
                 max_shape_components=[1, 2, 3],
                 max_appearance_components=[3, 3, 3],
                 boundary=3,
                 interpolator='scipy').build(training_images, group='PTS')


def test_aam_1():
    assert (aam.n_training_images == 2)
    assert (aam.n_levels == 3)
    assert (aam.downscale == 2)
    assert (aam.feature_type[0] == 'igo' and aam.feature_type[2] is None)
    assert (aam.interpolator == 'scipy')
    assert_allclose(np.around(aam.reference_shape.range()), (110., 102.))
    assert (not aam.scaled_shape_models)
    assert (np.all([aam.shape_models[j].n_components == 1
                    for j in range(aam.n_levels)]))
    assert (np.all([aam.appearance_models[j].n_components == 1
                    for j in range(aam.n_levels)]))
    assert_allclose([aam.appearance_models[j].template_instance.n_channels
                     for j in range(aam.n_levels)], (2, 2, 1))
    assert_allclose([aam.appearance_models[j].components.shape[1]
                     for j in range(aam.n_levels)], (13892, 13892, 6946))


@raises(ValueError)
def test_n_shape_exception():
    fitter = LucasKanadeAAMFitter(aam, n_shape=[3, 6, 'a'])


@raises(ValueError)
def test_n_appearance_exception():
    fitter = LucasKanadeAAMFitter(aam, n_appearance=[10, 20])


def test_pertrube_shape():
    fitter = LucasKanadeAAMFitter(aam)
    s = fitter.perturb_shape(training_images[0].landmarks['PTS'].lms,
                             noise_std=0.08, rotation=False)
    assert (s.n_dims == 2)
    assert (s.n_landmark_groups == 0)
    assert (s.n_points == 68)


def test_obtain_shape_from_bb():
    fitter = LucasKanadeAAMFitter(aam)
    s = fitter.obtain_shape_from_bb(np.array([[26, 49], [350, 400]]))
    assert ((np.around(s.points) == np.around(initial_shape[1].points)).
            all())
    assert (s.n_dims == 2)
    assert (s.n_landmark_groups == 0)
    assert (s.n_points == 68)


@raises(ValueError)
def test_n_appearance_exception():
    fitter = LucasKanadeAAMFitter(aam,
                                  algorithm=AlternatingInverseCompositional)
    fitter.fit(training_images[0], initial_shape[0],
               max_iters=[10, 20, 30, 40])


def run_test(aam=aam, algorithm=AlternatingInverseCompositional, im_number=0,
             max_iters=2, initial_error=0.04287, final_error=0.0103,
             error_type='me_norm'):
    fitter = LucasKanadeAAMFitter(aam, algorithm=algorithm)
    fitting_result = fitter.fit(
        training_images[im_number], initial_shape[im_number],
        gt_shape=training_images[im_number].landmarks['PTS'].lms,
        max_iters=max_iters, error_type=error_type)
    assert (np.around(fitting_result.initial_error, 5) == initial_error)
    assert (np.around(fitting_result.final_error, 5) == final_error)


def test_alternating_ic():
    run_test(aam, AlternatingInverseCompositional, 0, 6, 0.04287, 0.00041,
             'me_norm')


def test_adaptive_ic():
    run_test(aam, AdaptiveInverseCompositional, 1, 6, 58.78675, 57.12899, 'me')


def test_simultaneous_ic():
    run_test(aam, SimultaneousInverseCompositional, 0, 6, 12.66692, 0.14499,
             'rmse')


def test_projectout_ic():
    run_test(aam, ProjectOutInverseCompositional, 1, 6, 0.64101, 0.61362,
             'me_norm')


def test_alternating_fa():
    run_test(aam, AlternatingForwardAdditive, 1, 6, 0.64101, 0.4495, 'me_norm')


def test_adaptive_fa():
    run_test(aam, AdaptiveForwardAdditive, 0, 6, 0.04287, 0.0003, 'me_norm')


def test_simultaneous_fa():
    run_test(aam, SimultaneousForwardAdditive, 1, 6, 58.78675, 41.42773, 'me')


def test_projectout_fa():
    run_test(aam, ProjectOutForwardAdditive, 0, 6, 12.66692, 0.08345, 'rmse')


def test_alternating_fc():
    run_test(aam, AlternatingForwardCompositional, 0, 6, 12.66692, 0.22511,
             'rmse')


def test_adaptive_fc():
    run_test(aam, AdaptiveForwardCompositional, 1, 6, 0.64101, 0.50041,
             'me_norm')


def test_simultaneous_fc():
    run_test(aam, SimultaneousForwardCompositional, 0, 6, 0.04287, 0.00068,
             'me_norm')


def test_projectout_fc():
    run_test(aam, ProjectOutForwardCompositional, 1, 6, 58.78675, 45.89221,
             'me')
