import React from 'react';

/**
 * A container component that wraps around other components.
 */
export default class ContainerComponent extends React.Component {
    render() {
        return (
            <div className="my-3 p-3 bg-white rounded">
                <h6 className="border-bottom border-gray pb-2 mb-0">{this.props.title}</h6>
                {this.props.children}
            </div>
        );
    }
}