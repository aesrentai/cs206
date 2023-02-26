import React, { Component } from 'react';
import './chatinstance.css';
import axios from "axios";

interface ChatInstanceFormProps {
  userText: string;
}

interface ChatInstanceFormState {
  facts: SingleFact[]
}

interface Source {
  url: string,
  title: string,
  description: string,
}

interface SingleFact {
  fact: string,
  sources: Source[]
}

class FactDisplay extends Component<{fact: SingleFact}, {}> {
  render() {
    return (
      <ul>
        {this.props.fact.sources.map(fact =>{return (<li>fact</li>)})}
      </ul>
    );
  }
}

class ChatInstance extends Component<ChatInstanceFormProps, ChatInstanceFormState> {
  constructor(props: ChatInstanceFormProps) {
    super(props);
    this.state = {
      facts: [] as SingleFact[],
    };
  }

  // make api call here
  async componentDidMount() {
    // stop hardcoding this
    try {
      const url = "http://localhost:40000";
      const config = {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json'
        }
      };
      const response = await axios.post<SingleFact[]>(
        url,
        {text: this.props.userText},
        config
      );
      this.setState({facts: response.data});
      console.log("DATA BELOW");
      console.log(response.data);
    } catch(error) {
      console.log(error)
    }
  }

  render() {
    return (
      <div>
        <div className="chat">
          <div className="profile">
            <img src="/default_pfp.png" alt="Profile" />
          </div>
          <div className="message">
            <p>{this.props.userText}</p>
          </div>
        </div>
        <div className="ai text-wrapper">
          <div className="chat">
            <div className="profile">
              <img src="/default_pfp.png" alt="Profile" />
            </div>
            <div className="message">
              {this.state.facts && Object.entries(this.state.facts)
                .map( ([key, value]) => {
                  return (
                    <div>
                      <p>Fact: {value.fact}</p>
                      <ul>
                        {value.sources.map(source => (
                          <li>
                            <a href={source.url} className="link">
                              <p className="title">{source.title}</p>
                              <p className="url">{source.url}</p>
                              <p className="desc"></p>
                            </a>
                          </li>
                        ))}
                      </ul>
                      <br />
                    </div>
                  )
                })
              }
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ChatInstance;
