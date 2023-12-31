

var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};


dagcomponentfuncs.CustomTooltip = function (props) {
    info = [
        React.createElement('div', {}, props.data.summary),
    ];
    return React.createElement(
        'div',
        {
            style: {
                border: '2pt solid white',
                backgroundColor: props.color || 'white',
                padding: 10,
            },
        },
        info
    );
};
