import React, { Component } from 'react';
import './textinput.css';
import ChatInstance from './chatinstance'

interface TextInputFormProps {}

interface TextInputFormState {
  text: string;
  elements: JSX.Element[];
}

class TextInputForm extends Component<TextInputFormProps, TextInputFormState> {
  constructor(props: TextInputFormProps) {
    super(props);
    this.state = {
      text: '',
      elements: [] as JSX.Element[],
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(event: React.FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const newInstance = <ChatInstance userText={this.state.text} />

    // Handle form submission here
    this.setState((prevState) => ({
      text: '',
      elements: [...prevState.elements, newInstance],
    }))
  }

  handleChange(event: React.ChangeEvent<HTMLTextAreaElement>): void {
    this.setState({ text: event.target.value });
  }

  render() {
    return (
      <div id="text-input-wrapper">
        <div id="chat_container">
          <div className="wrapper">
            {this.state.elements.length != 0 && this.state.elements.map((element, i) => (
              <div key={i}>{element}</div>
            ))}
          </div>
        </div>
        <form onSubmit={this.handleSubmit}>
          <textarea
            name="text"
            value={this.state.text}
            onChange={this.handleChange}
            placeholder="Enter your ChatGPT output here:"
            rows={1}
          />
          <button type="submit">
            <img src="/send.png" alt="Send" />
          </button>
        </form>
      </div>
    );
  }
}

export default TextInputForm;
