import streamlit as st

st.set_page_config(page_title="쇼핑 리스트", page_icon="🛒")

if "shopping_items" not in st.session_state:
    st.session_state.shopping_items = []  # [{"id": int, "text": str, "checked": bool}, ...]
if "next_id" not in st.session_state:
    st.session_state.next_id = 0
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None


def add_item(text):
    text = text.strip()
    if not text:
        return
    st.session_state.shopping_items.append(
        {"id": st.session_state.next_id, "text": text, "checked": False}
    )
    st.session_state.next_id += 1


def handle_add():
    add_item(st.session_state.new_item_input)
    st.session_state.new_item_input = ""


def delete_item(item_id):
    st.session_state.shopping_items = [
        item for item in st.session_state.shopping_items if item["id"] != item_id
    ]
    if st.session_state.editing_id == item_id:
        st.session_state.editing_id = None
    st.session_state.pop(f"edit_input_{item_id}", None)
    st.session_state.pop(f"check_{item_id}", None)


def start_edit(item_id):
    st.session_state.editing_id = item_id


def save_edit(item_id):
    key = f"edit_input_{item_id}"
    new_text = st.session_state.get(key, "").strip()
    for item in st.session_state.shopping_items:
        if item["id"] == item_id:
            if new_text:
                item["text"] = new_text
            break
    st.session_state.pop(key, None)
    st.session_state.editing_id = None


def cancel_edit():
    if st.session_state.editing_id is not None:
        st.session_state.pop(f"edit_input_{st.session_state.editing_id}", None)
    st.session_state.editing_id = None


def toggle_item(item_id):
    checked = st.session_state.get(f"check_{item_id}", False)
    for item in st.session_state.shopping_items:
        if item["id"] == item_id:
            item["checked"] = checked
            break


st.title("🛒 쇼핑 리스트")
st.caption("살 것을 추가하고, 산 건 체크하세요.")

input_col, button_col = st.columns([4, 1])
with input_col:
    st.text_input(
        "아이템 입력",
        label_visibility="collapsed",
        placeholder="아이템을 입력하세요 (예: 우유 1L)",
        key="new_item_input",
        on_change=handle_add,
    )
with button_col:
    st.button("➕ 추가", use_container_width=True, on_click=handle_add)

st.divider()

if not st.session_state.shopping_items:
    st.info("📭 추가된 아이템이 없습니다. 위 입력창에서 아이템을 추가해보세요.")
else:
    for item in st.session_state.shopping_items:
        item_id = item["id"]

        with st.container(border=True):
            if st.session_state.editing_id == item_id:
                edit_col, save_col, cancel_col = st.columns([5, 1, 1])
                with edit_col:
                    st.text_input(
                        "수정",
                        value=item["text"],
                        key=f"edit_input_{item_id}",
                        label_visibility="collapsed",
                    )
                with save_col:
                    st.button(
                        "💾 저장",
                        key=f"save_{item_id}",
                        use_container_width=True,
                        on_click=save_edit,
                        args=(item_id,),
                    )
                with cancel_col:
                    st.button(
                        "✖️ 취소",
                        key=f"cancel_{item_id}",
                        use_container_width=True,
                        on_click=cancel_edit,
                    )
            else:
                check_col, text_col, edit_col, delete_col = st.columns([0.6, 5, 1, 1])
                with check_col:
                    st.checkbox(
                        "완료",
                        value=item["checked"],
                        key=f"check_{item_id}",
                        label_visibility="collapsed",
                        on_change=toggle_item,
                        args=(item_id,),
                    )
                with text_col:
                    if item["checked"]:
                        st.markdown(f":gray[~~{item['text']}~~]")
                    else:
                        st.markdown(item["text"])
                with edit_col:
                    st.button(
                        "✏️ 수정",
                        key=f"edit_{item_id}",
                        use_container_width=True,
                        on_click=start_edit,
                        args=(item_id,),
                    )
                with delete_col:
                    st.button(
                        "🗑️ 삭제",
                        key=f"delete_{item_id}",
                        use_container_width=True,
                        on_click=delete_item,
                        args=(item_id,),
                    )
