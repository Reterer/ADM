%%writefile modules/utils.py
"""
Contains various utility functions for PyTorch model training and saving.
"""
import torch
from pathlib import Path
import pandas as pd

def max_length(df, column_name='Desrciption'):
    """
    Функция для определения максимальной длины строки в колонке датафрейма
    
    Параметры:
    df (pandas.DataFrame): Датафрейм
    column_name (str): Название колонки, для которой нужно определить максимальную длину
    
    Возвращает:
    int: Максимальная длина строки в колонке датафрейма
    """
    max_len = 0
    for text in df[column_name]:
        if len(text) > max_len:
            max_len = len(text)
    return max_len

def truncate(df, length, column_name='Desrciption'):
    """
    Функция для обрезания всех значений в колонке датафрейма до заданной длины
    
    Параметры:
    df (pandas.DataFrame): Датафрейм
    column_name (str): Название колонки, которую нужно обрезать
    length (int): Длина, до которой нужно обрезать строки
    
    Возвращает:
    pandas.DataFrame: Датафрейм с обрезанными строками в колонке
    """
    df_truncated = df.copy()
    df_truncated[column_name] = df_truncated[column_name].apply(lambda x: x[:length])
    return df_truncated



def save_model(model: torch.nn.Module,
               target_dir: str,
               model_name: str):
  """Saves a PyTorch model to a target directory.

  Args:
    model: A target PyTorch model to save.
    target_dir: A directory for saving the model to.
    model_name: A filename for the saved model. Should include
      either ".pth" or ".pt" as the file extension.

  Example usage:
    save_model(model=model,
               target_dir="models",
               model_name="recsys_embed1.pth")
  """
  # Create target directory
  target_dir_path = Path(target_dir)
  target_dir_path.mkdir(parents=True,
                        exist_ok=True)

  # Create model save path
  assert model_name.endswith(".pth") or model_name.endswith(".pt"), "model_name should end with '.pt' or '.pth'"
  model_save_path = target_dir_path / model_name

  # Save the model state_dict()
  print(f"[INFO] Saving model to: {model_save_path}")
  torch.save(obj=model.state_dict(),
             f=model_save_path)