import pandas as pd

from src.ingestions.ingestion_csv import find_columns

QUESTION_ALIASES: set[str] = {"Question", "Q"}
ANSWER_ALIASES: set[str] = {"Answer", "A"}


def test_find_columns_with_exact_valid_aliases():
    df = pd.DataFrame({"Question": ["What is 2+2?"], "Answer": ["4"]})
    question_column_name, answer_column_name = find_columns(
        df, QUESTION_ALIASES, ANSWER_ALIASES
    )
    assert question_column_name == "Question"
    assert answer_column_name == "Answer"


def test_find_columns_with_lowercase_both_valid_aliases():
    df = pd.DataFrame({"question": ["What is 2+2?"], "answer": ["4"]})
    question_column_name, answer_column_name = find_columns(
        df, QUESTION_ALIASES, ANSWER_ALIASES
    )
    assert question_column_name == "Question"
    assert answer_column_name == "Answer"


def test_find_columns_with_different_register_both_valid_aliases():
    df = pd.DataFrame({"qUesTion": ["What is 2+2?"], "anSWer": ["4"]})
    question_column_name, answer_column_name = find_columns(
        df, QUESTION_ALIASES, ANSWER_ALIASES
    )
    assert question_column_name == "Question"
    assert answer_column_name == "Answer"


def test_find_columns_with_non_valid_aliases():
    df = pd.DataFrame({"smth": ["What is 2+2?"], "smth2": ["4"]})
    question_column_name, answer_column_name = find_columns(
        df, QUESTION_ALIASES, ANSWER_ALIASES
    )
    assert (question_column_name, answer_column_name) == (None, None)


def test_find_columns_with_one_valid_aliases():
    df = pd.DataFrame({"smth": ["What is 2+2?"], "Answer": ["4"]})
    question_column_name, answer_column_name = find_columns(
        df, QUESTION_ALIASES, ANSWER_ALIASES
    )
    assert (question_column_name, answer_column_name) == (None, "Answer")


def test_find_columns_with_whitespaces_valid_aliases():
    df = pd.DataFrame({" Question ": ["2+2?"], " Answer ": ["4"]})
    q_col, a_col = find_columns(df, QUESTION_ALIASES, ANSWER_ALIASES)
    assert (q_col, a_col) == ("Question", "Answer")


# тут проверку провести
"""
def test_find_columns_with_extra_valid_aliases():
    df = pd.DataFrame({"Question": ["2+2?"], "Q": ["duplicate"], "Answer": ["4"]})
    q_col, a_col = find_columns(df, QUESTION_ALIASES, ANSWER_ALIASES)
    assert q_col == "Question"
    assert a_col == "Answer"
"""


def test_find_columns_extra_unrelated_noise():
    df = pd.DataFrame({"Question": ["2+2?"], "Answer": ["4"], "Extra": ["noise"]})
    q_col, a_col = find_columns(df, QUESTION_ALIASES, ANSWER_ALIASES)
    assert (q_col, a_col) == ("Question", "Answer")


def test_empty_dataframe():
    df = pd.DataFrame()
    q_col, a_col = find_columns(df, QUESTION_ALIASES, ANSWER_ALIASES)
    assert (q_col, a_col) == (None, None)


"""
def test_numeric_columns():
    df = pd.DataFrame({123: ["2+2?"], "Answer": ["4"]})
    q_col, a_col = find_columns(df, QUESTION_ALIASES, ANSWER_ALIASES)
    assert (q_col, a_col) == (None, "Answer")
"""
