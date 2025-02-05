import streamlit as st
import numpy as np
from video_processing import enhance_video
from config import EXAMPLES

st.set_page_config(
    page_title="Сверточный Видоусилитель",
    page_icon="🎬",
    layout="wide"
)


def main():
    st.title("🎬 Сверточный Видоусилитель")

    if 'current_filter' not in st.session_state:
        st.session_state.current_filter = "Повышение резкости"
        st.session_state.kernel = EXAMPLES["Повышение резкости"]

    # Секция загрузки файла
    uploaded_file = st.file_uploader("📤 Загрузите видео файл", type=["mp4", "avi", "mov"])

    # Панель управления фильтрами
    with st.sidebar:
        st.header("⚙ Настройки свертки")

        # Отображение текущего фильтра
        st.markdown(f"**Активный фильтр:** `{st.session_state.current_filter}`")
        kernel_input = st.text_input(
            "Матрица 3x3 (9 чисел через запятую):",
            value=", ".join(map(str, st.session_state.kernel.flatten())),
            help="Пример: -1, -1, -1, -1, 9, -1, -1, -1, -1",
            key="kernel_input"
        )

        st.subheader("📚 Пресеты фильтров")
        cols = st.columns(2)
        for idx, (name, example) in enumerate(EXAMPLES.items()):
            with cols[idx % 2]:
                is_active = name == st.session_state.current_filter
                btn_label = f"✅ {name}" if is_active else f"⚙️ {name}"
                if st.button(
                        btn_label,
                        help=f"Матрица: {example.tolist()}",
                        use_container_width=True
                ):
                    st.session_state.current_filter = name
                    st.session_state.kernel = example
                    st.rerun()

    if uploaded_file:
        if st.button("🚀 ПРИМЕНИТЬ СВЕРТОЧНЫЙ ФИЛЬТР", use_container_width=True, type="primary"):
            try:
                if not kernel_input.strip():
                    st.error("❌ Выберите фильтр или введите свою матрицу!")
                    return

                kernel_values = [float(x.strip()) for x in kernel_input.split(',')]

                if len(kernel_values) != 9:
                    st.error("❌ Требуется ровно 9 значений через запятую!")
                    return

                if all(abs(x) < 0.0001 for x in kernel_values):
                    st.error("❌ Матрица не может быть нулевой!")
                    return

                kernel = np.array(kernel_values).reshape(3, 3)
                st.session_state.kernel = kernel
                st.session_state.current_filter = "Пользовательский"

                with st.spinner("🔎 Применяем сверточный фильтр..."):
                    processed_path = enhance_video(uploaded_file, kernel)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Исходное видео")
                    st.video(uploaded_file)

                with col2:
                    st.subheader("Результат обработки")
                    st.video(processed_path)

                    with open(processed_path, "rb") as f:
                        st.download_button(
                            label="💾 Скачать результат",
                            data=f,
                            file_name="conv_video.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"⚠️ Критическая ошибка: {str(e)}")


if __name__ == "__main__":
    main()