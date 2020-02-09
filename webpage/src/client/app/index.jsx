import React from 'react';
import { render } from 'react-dom';

import CommitChart from './CommitChart.jsx';
import ContainerComponent from './ContainerComponent.jsx';
import ContributionChart from './ContributionChart.jsx';
import ContributionTree from './ContributionTree.jsx';
import ActivityMatrix from './ActivityMatrix.jsx';

class App extends React.Component {
    render() {
        return (
            <div>
                <ContainerComponent title={"Contribution Types"}>
                    <ContributionChart/>
                </ContainerComponent>

                <ActivityMatrix/>

                <ContainerComponent title={"Files & Folder Contribution"}>
                    <ContributionTree/>
                </ContainerComponent>

                <ContainerComponent title={"Overall Commit Distribution"}>
                    <CommitChart/>
                </ContainerComponent>

                <div className="my-3 p-3 bg-white rounded footer">
                    Created by <a href="https://github.com/kelhaji" target="_blank"
                                  rel="noopener noreferrer">@kelhaji</a> on GitHub. Icon
                    used in logo made by Freepik from <a href="http://www.flaticon.com/"
                                                         target="_blank"
                                                         rel="noopener noreferrer">www.flaticon.com</a>.
                </div>
            </div>
        );
    }
}

render(<App/>, document.getElementById('app'));