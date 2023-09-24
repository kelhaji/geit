import CommitChart from './components/Commit/CommitChart.jsx';
import ContainerComponent from './components/ContainerComponent.jsx';
import ContributionChart from './components/Contribution/ContributionChart.jsx';
import ContributionTree from './components/Contribution/ContributionTree.jsx';
import ActivityMatrix from './components/ActivityMatrix.jsx';

function App() {
  const geitData = window.geitData || JSON.parse(process.env.REACT_APP_EXAMPLE_DATA);

  return (
    <div>
      <ContainerComponent title={"Contribution Types"}>
          <ContributionChart data={geitData} />
      </ContainerComponent>

      {geitData.matrix ? <ActivityMatrix data={geitData}/> : null}

      <ContainerComponent title={"Files & Folder Contribution"}>
          <ContributionTree data={geitData}/>
      </ContainerComponent>

      <ContainerComponent title={"Overall Commit Distribution"}>
          <CommitChart data={geitData}/>
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

export default App;
