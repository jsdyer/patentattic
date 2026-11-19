const sections = {
  A: 'A · Human necessities', B: 'B · Operations and transport', C: 'C · Chemistry and metallurgy',
  D: 'D · Textiles and paper', E: 'E · Fixed constructions', F: 'F · Mechanical engineering',
  G: 'G · Physics', H: 'H · Electricity',
};

export function preGrantCatalog(edition) {
  const records = edition.rows.map(([number, title, applicant, ipc, date, position, note]) => {
    const review = note ? note.split(' / ').at(-1) : 'No status note';
    return {
      title, date, summary: applicant, highlight: number, kicker: ipc + ' / Pre-grant application',
      a: sections[ipc[0]] ?? ipc[0], b: review, c: '', keywords: [number, ipc, applicant].join(' '),
      fields: {'Application number': number, 'Applicant': applicant, 'IPC classification': ipc,
        'Final fee received': date, 'Queue position in this edition': position, 'Workbook status note': review},
      links: [{label: 'Canadian Patents Database record', url: 'https://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/patent/' + number + '/summary.html'}],
    };
  });
  return {slug:'patentattic-pregrants', updated:edition.updated, records,
    coverage:edition.count.toLocaleString('en-CA') + ' pre-grant applications',
    facets:['IPC section','Workbook status note',null], examples:['Lidar','Gearing system','G01S','Optical'],
    method:'CIPO orders this list by receipt of the final fee. The date shown on each card is the final fee date. A listing records a pending application at the workbook date. Check the official record for a later grant or other change.',
    sources:[{label:'CIPO pre-grant list and definitions',url:edition.source},{label:'Original workbook',url:edition.workbook}]};
}
