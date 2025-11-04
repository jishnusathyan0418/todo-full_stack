import styles from '../styles/todo-list.module.css'
import { useState, useEffect, useCallback, useRef } from 'react'
import { debounce } from 'lodash'
import ToDo from './todo'






export default function ToDoList() {
    const [todos, setTodos] = useState(null)
    const [mainInput, setMainInput] = useState('')
    const [filter, setFilter] = useState()
    const didFetchRef = useRef(false)

    console.log("=== DEBUG INFO ===")
    console.log("API URL from env:", process.env.NEXT_PUBLIC_API_URL)
    console.log("Type:", typeof process.env.NEXT_PUBLIC_API_URL)
    console.log("==================")


// Fetching Data: Getting the Initial To-Do List
    useEffect(() => {
        if (didFetchRef.current == false) {
            didFetchRef.current = true
            fetchTodos()
        }
    }, [])

    async function fetchTodos(completed) {
        let path = '/todos'
        if (completed !== undefined) {
            path = `/todos?completed=${completed}`
        }
        const res = await fetch(process.env.NEXT_PUBLIC_API_URL + path)
        const json = await res.json()
        console.log("Fetched todos:", json) 
        setTodos(json.detail || json || [])
    }
    
    
    // 4. ✍️ Updating a To-Do: Handling Changes

    const debounceUpdatedTodo = useCallback(debounce(updateTodo, 500), [])

    function handleToChange(e, id) {
        const target = e.target
        const value = target.type === 'checkbox' ? target.checked : target.value
        const name  = target.name
        const copy = [...todos]
        const idx = copy.findIndex((todo => todo.id === id))
        const changedTodo = {
            ...todos[idx],
            [name]: value
        }
        copy[idx] = changedTodo
        debounceUpdatedTodo(changedTodo)
        setTodos(copy)
    }

    async function updateTodo(todo) {
        const data = {
            name: todo.name,
            completed: todo.completed
        }
        const res = await fetch(process.env.NEXT_PUBLIC_API_URL + `/todos/${todo.id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        })
    }

// ➕ Part 5: Adding & Deleting To-Dos
    async function addTodo(name) {
        const res = await fetch(process.env.NEXT_PUBLIC_API_URL + '/todos', {
            method: 'POST',
            body: JSON.stringify({
                name: name,
                completed: false
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        if (res.ok) {
            const json = await res.json()
            const copy = [...todos, json]
            setTodos(copy)
        }
    }


    async function handleDeleteTodo(id) {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        if (res.ok) {
            const idx = todos.findIndex((todo) => todo.id === id)
            const copy = [...todos]
            copy.splice(idx, 1)
            setTodos(copy)
        }
    }

    // ⌨️ Part 6: Event Handlers - Responding to User Actions

    function handleMainInputChange(e) {
        setMainInput(e.target.value)
    }

    function handleKeyDown(e) {
        if (e.key == 'Enter') {
            if (mainInput.length > 0) {
                addTodo(mainInput)
                setMainInput('')
            }
        }
    }

    function handleFilterChange(value) {
        setFilter(value)
        fetchTodos(value)
    }


    // 🖥️ Part 7: The Return (JSX) - What Appears on the Screen

    return (
        <div className={styles.container}>
            <div className={styles.mainInputContainer}>
                <input className={styles.mainInput} placeholder='what needs to be done?' value={mainInput} onChange={(e) => handleMainInputChange(e)} onKeyDown={handleKeyDown}></input>
            </div>
            {!todos && (
                <div>Loading....</div>
            )}
            {todos && (
                <div>
                    {todos.map((todo) => {
                        return (
                            <ToDo key={todo.id} todo={todo} onDelete={handleDeleteTodo} onChange={
                                handleToChange
                            } />
                        )
                    })}
                </div>
            )}
            <div className={styles.filters}>
                <button className={`${styles.filterBtn} ${filter === undefined && styles.filterActive}`} onClick={() => handleFilterChange()}>All</button>
                <button className={`${styles.filterBtn} ${filter === false && styles.filterActive}`} onClick={() => handleFilterChange(false)}>Active</button>
                <button className={`${styles.filterBtn} ${filter === true && styles.filterActive}`} onClick={() => handleFilterChange(true)}>Completed</button>
            </div>
        </div>
    )
}

