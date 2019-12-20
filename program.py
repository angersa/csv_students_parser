import parse_1001


def main():
    parse_1001.init()

    echecs = parse_1001.trouve_echecs()
    print('Échecs : ')
    for etudiant in echecs:
        print(f'\t{etudiant.Nom}, {etudiant.Prenom}, {etudiant.total}%')

    parse_1001.print_stats()
    parse_1001.show_distribution()
    parse_1001.create_outout_file()


if __name__ == '__main__':
    main()