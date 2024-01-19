import numpy as np

from src.components.model_trainer import ModelTrainer


if __name__ == "__main__":

    bearing_num = 4

    trainer = ModelTrainer(bearing_num=bearing_num)

    X_train, X_val = trainer.prepare_training_data()

    params = {
        "n_estimators":100,
        "max_samples":'auto',
        "contamination": float(0.03),
        "max_features": 1.0,
        "bootstrap": True,
        "random_state": 42
    }

    model, y_pred_train, y_pred_val = trainer.train_model(X_train, X_val, params)

    y_pred_test = trainer.predict_test(model)

    y_preds_all = np.concatenate([y_pred_train, y_pred_val, y_pred_test], axis=0)

    print(f"Y predictions all: {y_preds_all}")

    trainer.save_predictions(data_filepath=f'artifacts/data/transformed/processed_data_b{bearing_num}.csv', y_preds=y_preds_all)

