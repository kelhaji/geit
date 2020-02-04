import React from 'react';

class ContainerComponent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {likesCount : 0};
    this.onLike = this.onLike.bind(this);
  }

  onLike () {
    let newLikesCount = this.state.likesCount + 1;
    this.setState({likesCount: newLikesCount});
  }

  render() {
    return (
        <div className="my-3 p-3 bg-white rounded">
          <h6 className="border-bottom border-gray pb-2 mb-0">{this.props.title}</h6>
          {this.props.children}
        </div>
    );
  }

}

export default ContainerComponent;