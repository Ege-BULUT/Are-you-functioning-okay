import streamlit as st
import json
from datetime import date

DATA_FILE = 'daily_stats.json'

def st_vertical_space(n):
    for i in range(n):
        st.write(" ")

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    cl = st.columns(2)
    with cl[0]:
        st.title("Daily Tracker")
    with cl[1]:
        st_vertical_space(2)
        all_stats = st.container()
    today = str(date.today())
    data = load_data()

    if today not in data:
        data[today] = {"water_consumption": 0, "work_hours": 0, "todo_tasks": []}

    water_container = st.container()
    work_container = st.container()
    todo_container = st.container()

    with water_container:
        st.header("Water Consumption")
        water_cols = st.columns(2)
        with water_cols[0]:
            water_consumption = st.number_input("Enter water consumption (in liters):", min_value=0.0, step=0.1)
            cols2 = st.columns([5,5,3])
            if cols2[0].button("Add+", key="add_water"):
                data[today]["water_consumption"] += water_consumption
                save_data(data)
                st.experimental_rerun()
            if cols2[1].button("Sub-", key="sub_water"):
                data[today]["water_consumption"] -= water_consumption
                save_data(data)
                st.experimental_rerun()
            if cols2[2].button("Set=", key="set_water"):
                data[today]["water_consumption"] = water_consumption
                save_data(data)
                st.experimental_rerun()

            if st.columns([4,10,4])[1].button("Add One Glass (200ml)"):
                data[today]["water_consumption"] += 0.2
                save_data(data)
                st.experimental_rerun()

        with water_cols[1]:
            st_vertical_space(2)
            st.write(f"Total Water Consumption: {data[today]['water_consumption']} / 2.5 liters")

    with work_container:
        st.header("Work Hours")
        work_cols = st.columns([3,1,4])
        work_hours_hours = work_cols[0].slider("Hours:", min_value=0, max_value=24, value=1)
        work_hours_minutes = work_cols[0].slider("Minutes:", min_value=0, max_value=59, value=0)
        with work_cols[1]:
            st_vertical_space(2)
            if st.button("Add+", key="add_work"):
                work_hours = work_hours_hours + work_hours_minutes / 60
                data[today]["work_hours"] += work_hours
                save_data(data)
                st.experimental_rerun()
            if st.button("Sub-", key="sub_work"):
                work_hours = work_hours_hours + work_hours_minutes / 60
                data[today]["work_hours"] -= work_hours
                save_data(data)
                st.experimental_rerun()
            if st.button("Set=", key="set_work"):
                work_hours = work_hours_hours + work_hours_minutes / 60
                data[today]["work_hours"] = work_hours
                save_data(data)
                st.experimental_rerun()

        with work_cols[2]:
            st_vertical_space(6)
            st.write(f"Total Work Hours: {data[today]['work_hours']} / 8 hours")

    with todo_container:
        st.header("Todo Tasks")
        task_cols = st.columns([19,1,20])
        with task_cols[0]:
            task = st.text_input("Enter a task:")
        if st.button("Add Task"):
            data[today]["todo_tasks"].append({"task": task, "completed": False})
            save_data(data)
            st.experimental_rerun()

        for i, task in enumerate(data[today]["todo_tasks"]):
            task_cols2 = st.columns([1, 15, 2])
            with task_cols2[1]:
                completed = st.checkbox(task["task"], value=task["completed"])
                data[today]["todo_tasks"][i]["completed"] = completed
            with task_cols2[2]:
                if st.button("❌", key=f"delete_task_{i}"):
                    data[today]["todo_tasks"].pop(i)
                    save_data(data)
                    st.experimental_rerun()

        save_data(data)

        with task_cols[2]:
            total_tasks = len(data[today]["todo_tasks"])
            completed_tasks = sum(1 for t in data[today]["todo_tasks"] if t["completed"])
            st_vertical_space(2)
            st.write(f"Total works done: {completed_tasks} / {total_tasks}")

    with all_stats:
        with st.expander("Today's Stats"):
            show_stats(data, today)

    st.subheader(" ", divider="rainbow")

    st.columns([115,200,85])[1].subheader("Today's Stats!")
    with st.columns([100,200,100])[1]:
        show_stats(data, today)

def show_stats(data, today):
    st.write(f"🥤 Water Consumption: {data[today]['water_consumption']} liters")
    st.write(f"💼 Work Hours: {data[today]['work_hours']} hours")
    st.write("📓 Todo Tasks:")
    for task in data[today]["todo_tasks"]:
        status = "✅" if task["completed"] else "❌"
        with st.columns([1,19])[1]:
            st.write(f"{status} {task['task']}")

if __name__ == "__main__":
    main()
