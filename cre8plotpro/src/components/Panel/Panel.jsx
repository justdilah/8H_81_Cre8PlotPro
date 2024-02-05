import React from "react";
import './Panel.css'
import {render} from "@testing-library/react";
const Panel = (props) => {

    // retrieve chatbot state
    const {setState} = props

    React.useEffect(()=>{
        fetch('https://jsonplaceholder.typicode.com/todos')
            .then(res => res.json())
            .then(data => {
                const fiveToDo = data.slice(0,5)
                setState(state => ({...state, panel: fiveToDo}))
            })
    }, [])

    const renderPanels = () => {
        return props.state.panel.map((panel) => {
          return (<li className="panels-widget-list-item" key={panel.id}>
              {panel.title}
          </li>);
        });
    };

    return(
        <div className='panel-widget'>
            <ul className="panel-widget-list">{renderPanels()}</ul>
        </div>
    )
}

export default Panel;