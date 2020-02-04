import React from 'react';
import {render} from 'react-dom';

// import AwesomeComponent from './AwesomeComponent.jsx';
import CommitChart from './CommitChart.jsx';
import ContainerComponent from './ContainerComponent.jsx';
import ContributionChart from './ContributionChart.jsx';
import ContributionTree from './ContributionTree.jsx';
import ActivityMatrix from './ActivityMatrix.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
        <ContainerComponent title={"Contribution Types"}>
            <ContributionChart />
        </ContainerComponent>

        <ActivityMatrix />

        <ContainerComponent title={"Contribution Tree"}>
            <ContributionTree />
        </ContainerComponent>

        <ContainerComponent title={"Overall Commit Distribution"}>
            <CommitChart />
        </ContainerComponent>
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));