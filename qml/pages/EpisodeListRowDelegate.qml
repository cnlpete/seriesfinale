import QtQuick 2.0
import Sailfish.Silica 1.0

BackgroundItem {
    id: epListItem
    width: ListView.view.width
    contentHeight: Theme.itemSizeSmall

    signal watchToggled(bool watched)
    property alias title: title.text
    property alias subtitle: subtitle.text
    property variant episode: undefined

    Row {
        anchors.fill: parent

        Switch {
            id: markItem
            anchors.verticalCenter: parent.verticalCenter
            checked: episode.isWatched

            onClicked: {
                epListItem.watchToggled(checked)
            }
        }

        Column {
            id: column
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width - markItem.width - Theme.horizontalPageMargin

            Label {
                id: title
                width: parent.width
                font.pixelSize: Theme.fontSizeSmall
                color: episode.isWatched ? Theme.secondaryColor : episode.hasAired ? Theme.primaryColor : Theme.secondaryColor
                text: episode.episodeName
                truncationMode: TruncationMode.Fade
            }

            Label {
                id: subtitle
                font.pixelSize: Theme.fontSizeTiny
                color: Theme.secondaryColor
                text: episode.airDate
                visible: text != ""
            }
        }
    }
}
