import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from src.constants import constants


# Callback to save images during training
# class SaveImageTraining(tf.keras.callbacks.Callback):
#     """
#     Callback para guardar imágenes generadas durante el entrenamiento
#
#     Attributes:
#     ___________
#         X: np.ndarray
#             Array of images
#         y: np.ndarray
#             Array of labels
#         save_dir: str
#             Directory to save images
#
#     Methods:
#     ________
#         on_epoch_end(self, epoch, logs=None)
#             Saves images generated by the model at the end of each epoch
#
#     Examples:
#     _________
#     Creamos la instancia del callback y le indicamos el directorio donde guardar las imágenes:
#
#     >>> save_callback = SaveImageTraining(X, y_encoded, save_dir="generated_images")
#
#     Entrenamos la GAN con el callback:
#
#     >>> gan = cGAN()
#
#     >>> gan.fit(X, y_encoded, epochs=100, batch_size=32, callbacks=[save_callback])
#     """
#
#     def __init__(self, X: np.ndarray, y: np.ndarray, save_dir: str = "generated_images"):
#         """
#
#         Parameters:
#         ___________
#             X: np.ndarray
#                 Array of images
#             y: np.ndarray
#                 Array of labels
#             save_dir: str
#                 Directory to save images
#         """
#         super().__init__()
#         self.X = X
#         self.y = y
#         self.save_dir = save_dir
#
#     def on_epoch_end(self, epoch, logs=None):
#         # Labels for generated images
#         n = len(np.unique(self.y))
#         [rows, cols, _] = self.X.shape[1:]
#         latent_dim = self.model.generator.input_shape[0][1]
#         labels = np.expand_dims(np.array([x for _ in range(n) for x in range(3)]), axis=-1)
#         noise_input = np.random.randn(latent_dim * n * 3).reshape(n * 3, latent_dim)
#         fake_img = self.model.generator([noise_input, labels], training=False)
#         real_img = np.zeros((n, rows, cols))
#         random_idx = np.random.randint(0, self.X.shape[0] / n)
#         for label in range(n):
#             real_img[label] = self.X[np.where(self.y == label)[0], :, :, 0][random_idx]
#
#         # Plot generated vs real images
#         fig, axs = plt.subplots(3, n, figsize=(30, 10), dpi=100)
#         for i in range(n):
#             axs[0, i].imshow(real_img[i], cmap='seismic', vmin=-1, vmax=1);
#             axs[0, i].invert_xaxis()
#             axs[0, i].invert_yaxis()
#             axs[0, i].set_title('Real {}, epoch {:04d}'.format(constants.dictionary_decoding[i], epoch))
#             axs[1, i].imshow(fake_img[i].numpy(), cmap='seismic', vmin=-1, vmax=1)
#             axs[1, i].invert_xaxis()
#             axs[1, i].invert_yaxis()
#             axs[1, i].set_title('Generated {}, epoch {:04d}'.format(constants.dictionary_decoding[i], epoch))
#             axs[2, i].hist(fake_img[i].numpy().flatten(), bins=100, density=True, alpha=0.5, label="Generated")
#             axs[2, i].set_title('Hist fake {}, epoch {:04d}'.format(constants.dictionary_decoding[i], epoch))
#             axs[2, i].set_xlim((-1, 1))
#
#         plt.tight_layout()
#         plt.savefig(f'{self.save_dir}/generated_plot_epoch_%04d.png' % (epoch + 1))
#         plt.close()

class SaveImageTraining(tf.keras.callbacks.Callback):
    """
    Callback para guardar imágenes generadas durante el entrenamiento

    Attributes:
    ___________
        X: np.ndarray
            Array of images
        y: np.ndarray
            Array of labels
        save_dir: str
            Directory to save images

    Methods:
    ________
        on_epoch_end(self, epoch, logs=None)
            Saves images generated by the model at the end of each epoch

    Examples:
    _________
    Creamos la instancia del callback y le indicamos el directorio donde guardar las imágenes:

    >>> save_callback = SaveImageTraining(X, y_encoded, save_dir="generated_images")

    Entrenamos la GAN con el callback:

    >>> gan = cGAN()

    >>> gan.fit(X, y_encoded, epochs=100, batch_size=32, callbacks=[save_callback])
    """

    def __init__(self, X: np.ndarray, y: np.ndarray, save_dir: str = "generated_images"):
        """

        Parameters:
        ___________
            X: np.ndarray
                Array of images
            y: np.ndarray
                Array of labels
            save_dir: str
                Directory to save images
        """
        super().__init__()
        self.X = X
        self.y = y
        self.save_dir = save_dir

    def on_epoch_end(self, epoch, logs=None):
        # Labels for generated images
        n = len(np.unique(self.y))
        [rows, cols, _] = self.X.shape[1:]
        latent_dim = self.model.generator.input_shape[0][1]
        labels = np.expand_dims(np.array([x for x in range(n)]), axis=-1)
        noise_input = np.random.randn(latent_dim * n).reshape(n, latent_dim)
        fake_img = self.model.generator([noise_input, labels], training=False)
        real_img = np.zeros((n, rows, cols))
        random_idx = np.random.randint(0, self.X.shape[0] / n)
        for label in range(n):
            real_img[label] = self.X[np.where(self.y == label)[0], :, :, 0][random_idx]

        # Plot generated vs real images
        fig, axs = plt.subplots(3, n, figsize=(30, 10), dpi=100)
        for i in range(n):
            axs[0, i].imshow(real_img[i], cmap='seismic', vmin=-1, vmax=1);
            axs[0, i].invert_xaxis()
            axs[0, i].invert_yaxis()
            axs[0, i].set_title('Real {}, epoch {:04d}'.format(constants.dictionary_decoding[i], epoch))
            axs[1, i].imshow(fake_img[i].numpy(), cmap='seismic', vmin=-1, vmax=1)
            axs[1, i].invert_xaxis()
            axs[1, i].invert_yaxis()
            axs[1, i].set_title('Generated {}, epoch {:04d}'.format(constants.dictionary_decoding[i], epoch))
            axs[2, i].hist(fake_img[i].numpy().flatten(), bins=100, density=True, alpha=0.5, label="Generated")
            axs[2, i].set_title('Hist fake {}, epoch {:04d}'.format(constants.dictionary_decoding[i], epoch))
            axs[2, i].set_xlim((-1, 1))

        plt.tight_layout()
        plt.savefig(f'{self.save_dir}/generated_plot_epoch_%04d.png' % (epoch + 1))
        plt.close()


class LoggingCheckpointTraining(tf.keras.callbacks.Callback):
    """
    Callback para guardar el modelo durante el entrenamiento

    Attributes:
    ___________
        save_dir: str
            Directorio donde guardar el modelo

    Methods:
    ________
        on_epoch_end(self, epoch, logs=None)
            Guarda el modelo al final de cada época

    Examples:
    _________
    Creamos la instancia del callback y le indicamos el directorio donde guardar el modelo:

    >>> checkpoint_callback = LoggingCheckpointTraining(save_dir="generator_model_checkpoint")

    Entrenamos la GAN con el callback:

    >>> gan = cGAN()

    >>> gan.fit(X, y_encoded, epochs=100, batch_size=32, callbacks=[checkpoint_callback])
    """
    def __init__(self, save_dir="generator_model_checkpoint"):
        super().__init__()
        self.save_dir = save_dir

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 10 == 0:
            self.model.generator.save(f'{self.save_dir}/c_gan%3d.h5' % epoch)
