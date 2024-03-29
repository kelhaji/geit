import React from 'react';
import Util from '../../logic/Util.js';

/**
 * Formats a number and returns a string.
 * 
 * @param {number} value 
 * @returns string
 */
const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`
};

/**
 * Recurses through the folder tree and adds the contributors to the store object, so we 
 * can determine the percentage on a folder level.
 * 
 * @param {object} folderTree 
 * @param {object} storeObject 
 */
const recurseFolderTree = (folderTree, storeObject) => {
    Object.keys(folderTree).forEach((key) => {
        if (folderTree[key].is_file === true) {
            if (folderTree[key].contributors) {
                Object.keys(folderTree[key].contributors).forEach((email) => {
                    if (!storeObject.hasOwnProperty(email)) {
                        storeObject[email] = 0;
                    }

                    storeObject[email] += folderTree[key].contributors[email];
                });
            }
        } else {
            recurseFolderTree(folderTree[key], storeObject);
        }
    })
};

/**
 * Fills the contributors array with the contributors of a file/folder including percentages.
 * 
 * @param {object} contributorData 
 * @param {array} contributors 
 */
const determineContributors = (contributorData, contributors) => {
    let sum = 0;

    if (contributorData && contributors) {
        Object.keys(contributorData).forEach((contributor) => {
            sum += contributorData[contributor];
        });

        Object.keys(contributorData).forEach((contributor) => {
            let contributionPercentage = contributorData[contributor] / sum;

            contributors.push({
                percentage: formatPercentage(contributionPercentage),
                value: contributionPercentage,
                name: Util.cutEmail(contributor)
            });
        });
    }
};

/**
 * Generates the folder tree.
 * 
 * @param {string} folderTree 
 * @param {func} accessSubFolder 
 * @returns rendered folder tree 
 */
const generateFolderTree = (folderTree, accessSubFolder) => {
    let topLevelEntities = Object.keys(folderTree);

    topLevelEntities.sort();

    // Sort the folders to the top, and the files to the bottom.
    topLevelEntities.sort((a, b) => {
        if (folderTree[a].is_file === true &&
            folderTree[b].is_file === undefined) {
            return 1;
        }

        if (folderTree[a].is_file === undefined
            && folderTree[b].is_file === true) {
            return -1;
        }

        return 0;
    });

    const folderContent = topLevelEntities.map((key, index) => {
        let contributors = [];

        if (folderTree[key].is_file === true) {
            determineContributors(folderTree[key].contributors, contributors);
        } else {
            let storeObject = {};

            recurseFolderTree(folderTree[key], storeObject);

            determineContributors(storeObject, contributors);
        }

        contributors.sort((a, b) => {
            return b.value - a.value;
        });

        const isFolder = folderTree[key].is_file !== true;

        return (
            <tr key={index} className={isFolder ? "tree-entity" : ""}
                onClick={() => isFolder ? accessSubFolder(key) : null}>
                <td className={!isFolder ? "tree-file" : ""}>
                    {isFolder ? <i className="fa fa-folder fa-fw"></i> :
                        <i className="fa fa-file-text-o fa-fw"></i>}
                    <span className={isFolder ? "underline-hover" : ""}>{key}</span>
                </td>
                <td>
                    {contributors.map((contributor, index) => {
                        return (
                            <span key={index} style={{color: "#707070"}}>
                    {contributor.name} (<b>{contributor.percentage}</b>)
                    <span>{index !== contributors.length - 1 ? ' | ' : ''}</span>
                  </span>
                        );
                    })}
                </td>
            </tr>
        );
    });

    return folderContent;
};

/**
 * Renders a clickable folder structure showing the contribution of each user per file/folder.
 */
export default class ContributionTree extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            tree: this.props.data.contribution.tree,
            path: '.'
        };
    }

    /**
     * Access a sub folder.
     * 
     * @param {string} subFolder 
     */
    accessSubFolder(subFolder) {
        this.setState({
            tree: this.state.tree[subFolder],
            path: this.state.path + '/' + subFolder
        });
    }

    /**
     * Backtrack to the parent folder.
     */
    backtrackSubFolder() {
        let path = this.state.path.split('/');

        let targetPath = path[path.length - 2];

        if (targetPath === '.') {
            this.setState({
                tree: this.props.data.contribution.tree,
                path: '.'
            });
        } else {
            path.shift();

            path.pop();

            // Based off https://stackoverflow.com/questions/37611143/access-json-data-with-string-path
            // I don't know how this works exactly, but it does.
            const folderTree = path.reduce((o, k) => {
                return o && o[k];
            }, this.props.data.contribution.tree);

            this.setState({
                tree: folderTree,
                path: './' + path.join('/')
            });
        }
    }

    render() {
        return (
            <div className="bordered-box">
                <table>
                    <colgroup>
                        <col style={{width: "15%"}}></col>
                        <col style={{width: "85%"}}></col>
                    </colgroup>
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Contributions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr className="tree-entity"
                        style={{display: this.state.path === '.' ? 'none' : ''}}>
                        <td colSpan="2" className="underline-hover"
                            onClick={this.backtrackSubFolder.bind(this)}>..
                        </td>
                    </tr>
                    {generateFolderTree(this.state.tree, this.accessSubFolder.bind(this))}
                    </tbody>
                </table>
            </div>
        );
    }
}